import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ucimlrepo import fetch_ucirepo
  
# fetch dataset 
bank_marketing = fetch_ucirepo(id=222) 
  
# data (as pandas dataframes) 
X = bank_marketing.data.features 
y = bank_marketing.data.targets 
  
# metadata 
print(bank_marketing.metadata) 
  
# variable information 
print(bank_marketing.variables) 

df = X.copy()       # make a copy of features
df["y"] = y 

print("Dataset shape:", df.shape)
print(df.head())

# basic info
print("\nData types and non-null counts:")
print(df.info())

print("\nSummary statistics:")
print(df.describe(include='all').T)

# missing values & duplicates
print("\nMissing values per column:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

# target distribution
print("\nTarget distribution:")
print(df['y'].value_counts())
print(df['y'].value_counts(normalize=True))

# numeric distributions + boxplots
num_cols = df.select_dtypes(include=['int64','float64']).columns
for c in num_cols:
    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    sns.histplot(df[c], kde=True, bins=30)
    plt.title(f"Distribution of {c}")
    plt.subplot(1,2,2)
    sns.boxplot(x=df[c])
    plt.title(f"Boxplot of {c}")
    plt.tight_layout()
    plt.show()

# correlation heatmap (numeric only)
plt.figure(figsize=(10,8))
corr = df[num_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation Heatmap")
plt.show()

# categorical variable counts
cat_cols = df.select_dtypes(include=['object']).columns.drop('y')
for c in cat_cols:
    plt.figure(figsize=(8,4))
    sns.countplot(y=c, data=df, order=df[c].value_counts().index)
    plt.title(f"Distribution of {c}")
    plt.tight_layout()
    plt.show()

# relationship between categorical features and target
for c in cat_cols:
    ct = pd.crosstab(df[c], df['y'], normalize='index') * 100
    ct.plot(kind='bar', stacked=True, figsize=(8,4))
    plt.title(f"% Subscribed (y) by {c}")
    plt.ylabel("Percent")
    plt.tight_layout()
    plt.show()
