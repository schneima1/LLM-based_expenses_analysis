import abc
import pandas as pd
import numpy as np
import ollama
import re
from typing import List, Dict, Optional
from openai import OpenAI

class TransactionClassifier(abc.ABC):
    DEFAULT_EXPENSE_CATEGORIES = {
        "Wohnen": "Miete, Strom, Internet, Heizung, Nebenkosten, Vodafone, immergruen, Rundfunkbeitrag",
        "Mobilität": "Bahn, Auto, Tankstelle, Bus, Flug, DB, Tesla, EnBW",
        "Essen unterwegs": "Restaurant, Lieferdienst, Fast Food, Döner, Pizza",
        "Essen daheim": "Supermarkt, Lebensmittel, REWE, Aldi, Lidl, Edeka",
        "Investments": "ETF, Aktie, Trade Republic, Depot, Kryptowährung, Sparplan",
        "Freizeit & Lifestyle": "Kino, Konzert, Reisen, Sport, Amazon, Handy, Mobilfunk, Lebara, sim.de",
        "Urlaub": "Reise, Hotel, Flug, Mietwagen, booking, airbnb",
        "Versicherungen": "Lebensversicherung, Hausratversicherung, Kfz-Versicherung, Allianz, Getsafe, Itzehoer",
        "Kleidung & Körperpflege": "Friseur, Kosmetik, Mode, Klamotten, Fashion, Zara, H&M",
        "Sonstige": "divers, unbekannt"
    }

    DEFAULT_INCOME_CATEGORIES = {
        "Gehalt": "Lohn, Gehalt, Bezüge",
        "Mieteinnahmen": "Miete, Mieteingang",
        "Dividende": "Dividende, Ausschüttung",
        "Zinsen": "Zinsen, Zinsertrag",
        "Schenkungen": "Geschenk, Schenkung",
        "Sonstige": "Sonstige, diverse, Gutschrift"
    }

    def __init__(self, expense_categories: Optional[Dict[str, str]] = None, income_categories: Optional[Dict[str, str]] = None, model_name: str = "", base_url: Optional[str] = None):
        self.expense_categories = expense_categories or self.DEFAULT_EXPENSE_CATEGORIES
        self.income_categories = income_categories or self.DEFAULT_INCOME_CATEGORIES
        self.model_name = model_name
        self.base_url = base_url
        
        if base_url:
            self.client = OpenAI(base_url=base_url, api_key="flm")
        else:
            self.client = None

    @abc.abstractmethod
    def classify(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        pass

class EmbeddingClassifier(TransactionClassifier):
    def __init__(self, expense_categories: Optional[Dict[str, str]] = None, income_categories: Optional[Dict[str, str]] = None, model_name: str = "nomic-embed-text-v2-moe", base_url: Optional[str] = None):
        super().__init__(expense_categories, income_categories, model_name, base_url)
        self.category_embeddings = {}
        self.income_category_embeddings = {}
        self._precalculate_category_embeddings()

    def _get_embedding(self, text: str) -> Optional[np.ndarray]:
        try:
            if self.client:
                response = self.client.embeddings.create(model=self.model_name, input=text)
                return np.array(response.data[0].embedding)
            else:
                response = ollama.embeddings(model=self.model_name, prompt=text)
                return np.array(response['embedding'])
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None

    def _precalculate_category_embeddings(self):
        """
        Calculates embeddings for each keyword in the category description for better granularity.
        """
        # Precalculate for expense categories
        for cat_name, cat_desc in self.expense_categories.items():
            self.category_embeddings[cat_name] = self._calculate_embs(cat_name, cat_desc)
            
        # Precalculate for income categories
        for cat_name, cat_desc in self.income_categories.items():
            self.income_category_embeddings[cat_name] = self._calculate_embs(cat_name, cat_desc)

    def _calculate_embs(self, name: str, desc: str) -> List[np.ndarray]:
        name_emb = self._get_embedding(name)
        embs = [name_emb] if name_emb is not None else []
        keywords = [k.strip() for k in desc.split(',')]
        for kw in keywords:
            if kw:
                kw_emb = self._get_embedding(kw)
                if kw_emb is not None:
                    embs.append(kw_emb)
        return embs

    def _cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def classify(self, df: pd.DataFrame, exclude_internal: bool = True, **kwargs) -> pd.DataFrame:
        results = []
        for index, row in df.iterrows():
            if exclude_internal and row.get('Internal_Transfer', False):
                results.append("Internal Transfer")
                continue
                
            amount = row.get('Amount', 0)
            empfaenger = str(row.get('Account', ''))
            # Fallback to column index 2 if 'Account' is empty or NaN
            if not empfaenger or empfaenger.lower() == 'nan':
                if len(row) > 2:
                    val = row.iloc[2]
                    empfaenger = str(val) if pd.notna(val) else ''
            
            description = str(row.get('Description', ''))
            text = f"{empfaenger} {description}".strip()
            
            if not text:
                results.append("Sonstige")
                continue

            expense_emb = self._get_embedding(text)
            if expense_emb is None:
                results.append("Error")
                continue

            # Determine whether to use Income or Expense embeddings
            current_embeddings = self.income_category_embeddings if amount > 0 else self.category_embeddings
            
            best_cat = "Sonstige"
            max_sim = -1.0
            
            for cat_name, cat_embs in current_embeddings.items():
                for cat_emb in cat_embs:
                    sim = self._cosine_similarity(expense_emb, cat_emb)
                    if sim > max_sim:
                        max_sim = sim
                        best_cat = cat_name
            
            results.append(best_cat)
        
        df['Category'] = results
        return df

class LLMClassifier(TransactionClassifier):
    def __init__(self, system_prompt: str, expense_categories: Optional[Dict[str, str]] = None, income_categories: Optional[Dict[str, str]] = None, model_name: str = "gemma4:e4b", base_url: Optional[str] = None):
        super().__init__(expense_categories, income_categories, model_name, base_url)
        self.system_prompt = system_prompt

    def classify(self, df: pd.DataFrame, batch_size: int = 10, exclude_internal: bool = True, **kwargs) -> pd.DataFrame:
        df = df.copy()
        
        # Determine valid indices for classification
        if exclude_internal:
            to_classify_indices = df[~df['Internal_Transfer']].index.tolist()
        else:
            to_classify_indices = df.index.tolist()
            
        if not to_classify_indices:
            return df
            
        # Programmatically split into Expenses and Incomes
        expense_indices = [idx for idx in to_classify_indices if df.at[idx, 'Amount'] < 0]
        income_indices = [idx for idx in to_classify_indices if df.at[idx, 'Amount'] >= 0]
        
        results = {}
        
        # 1. Process Expenses first
        if expense_indices:
            print(f"Processing {len(expense_indices)} expenses...")
            results.update(self._process_group(df, expense_indices, self.expense_categories, batch_size, is_income=False))
            
        # 2. Process Incomes second
        if income_indices:
            print(f"Processing {len(income_indices)} incomes...")
            results.update(self._process_group(df, income_indices, self.income_categories, batch_size, is_income=True))
        
        # Assign categories to the dataframe
        for idx in df.index:
            if idx in results:
                df.at[idx, 'Category'] = results[idx]
            elif exclude_internal and df.at[idx, 'Internal_Transfer']:
                df.at[idx, 'Category'] = 'Internal Transfer'
                
        return df

    def _process_group(self, df: pd.DataFrame, indices: List[int], allowed_categories: Dict[str, str], batch_size: int, is_income: bool) -> Dict[int, str]:
        results = {}
        cat_list_str = ", ".join(allowed_categories.keys())
        
        # Build category descriptions including the keywords for guidance
        cat_details_str = "\n".join([f"- {name}: {desc}" for name, desc in allowed_categories.items()])
        
        group_type = "EINNAHMEN" if is_income else "AUSGABEN"
        
        for i in range(0, len(indices), batch_size):
            batch_idx = indices[i:i+batch_size]
            batch_data = []
            for idx in batch_idx:
                batch_data.append({
                    'amount': df.at[idx, 'Amount'],
                    'account': df.at[idx, 'Account'],
                    'description': df.at[idx, 'Description']
                })
            
            # Construct a dynamic prompt containing category keywords for guidance
            batch_text = "\n".join([
                f"{j+1}. Betrag: €{t['amount']:.2f}, Empfänger: {t['account']}, Text: {t['description']}"
                for j, t in enumerate(batch_data)
            ])
            
            specific_prompt = f"""Du bist ein Finanz-Assistent. Weise den folgenden {group_type} eine der Kategorien zu.
NUTZE NUR DIESE KATEGORIEN: {cat_list_str}

Kategorie-Beschreibungen zur Orientierung:
{cat_details_str}

Transaktionen:
{batch_text}

Antworte NUR mit der Liste der Kategorien im Format:
1. [Kategorie]
2. [Kategorie]
..."""
            
            # Call classifier
            cats = self._call_llm(specific_prompt)
            for j, cat in enumerate(cats):
                if j < len(batch_idx):
                    results[batch_idx[j]] = cat
                    
        return results

    def _call_llm(self, user_prompt: str) -> List[str]:
        try:
            if self.client:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                content = response.choices[0].message.content
            else:
                response = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                content = response['message']['content']
            
            categories = []
            for line in content.strip().split('\n'):
                # Extract category name after the number (e.g., "1. Food" -> "Food")
                # Handle cases like "1. Food: Description"
                clean_line = re.sub(r'^\d+\.\s*', '', line).split(':')[0].strip()
                if clean_line:
                    categories.append(clean_line)
            return categories
        except Exception as e:
            print(f"LLM Call Error: {e}")
            return []
