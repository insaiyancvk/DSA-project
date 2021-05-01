def get_str_dtype(df, col):
    """Return dtype of col in df"""
    dtypes = ['datetime', 'bool', 'int', 'float',
              'object', 'category']
    for d in dtypes:
        if d in str(df.dtypes.loc[col]).lower():
            return d