from sqlalchemy import inspect

def get_shema(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    shema = {}
    for table in tables:
        shema[table] = [col['name'] for col in inspector.get_columns(table)]
    return shema 


def get_descriptions(shema):
    descriptions = []
    for table,cols in shema.items():
        desc = f'Таблица {table} содержит колонки: {','.join(cols)}.'
        descriptions.append(desc)
    return descriptions   


if __name__ == '__main__':
    pass