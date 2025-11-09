from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent

def load_promt(name:str) ->str:
    """Загрузка txt промта"""
    path = PROMPTS_DIR/name
    if not path.exists():
        raise FileNotFoundError('Промт: {path} не найден')
    return path.read_text(encoding='UTF-8')

if __name__ == '__main__':
    pass