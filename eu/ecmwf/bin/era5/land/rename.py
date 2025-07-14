import pandas as pd
import numpy as np

# Load the meta file which contains id_old and id_new
meta = pd.read_csv('/media/windows/projects/bias_correction/applications/era5land/data/10years/OLD/pre_processed/meta.csv', index_col=0)

# Load the data file
data = pd.read_csv('/media/windows/projects/bias_correction/applications/era5land/data/10years/OLD/pre_processed/t_era5.csv', index_col=0)

# Rename the columns based on the id_mapping dictionary
# Exclude the first column which is 'datetime'
columns = []
values = []

for col in data.columns:
    try:
        id_new = meta.loc[int(col)].values[0]
    except:
        id_new = None

    if id_new != None:
        columns.append(id_new)
        values.append(data[col].values)

values = np.array(values)

new_df = pd.DataFrame(values.T, index=data.index, columns=columns)
ordered_ids = list(np.sort([i[0] for i in meta.values]))
new_df = new_df[ordered_ids]

# Save the updated data to a new CSV file
new_df.to_csv('/media/windows/projects/bias_correction/applications/era5land/data/10years/OLD/pre_processed/t_era5_renamed.csv')

print("Renaming complete. Output saved to 'data_renamed.csv'.")
