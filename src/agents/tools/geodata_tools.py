import os
import json
import csv
from langchain.tools import tool
import rasterio
import geopandas as gpd

def _read_text(path: str):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def _read_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _read_csv(path: str):
    rows = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    return rows

def _read_tiff_metadata(path: str):
    """
    Чтение только метаданных TIFF без пикселей.
    """
    try:
        with rasterio.open(path) as src:
            meta = {
                "width": src.width,
                "height": src.height,
                "count": src.count,
                "dtype": str(src.dtypes[0]),
                "crs": str(src.crs),
                "bounds": src.bounds._asdict(),
                "transform": list(src.transform),
                "driver": src.driver,
            }
            return meta
    except Exception as e:
        return {"error": f"Ошибка чтения TIFF: {e}"}
def _read_shapefile(path: str):
    """
    Возвращает только геометрии и атрибуты в GeoJSON.
    """
    try:
        gdf = gpd.read_file(path)
        return json.loads(gdf.to_json())
    except Exception as e:
        return {"error": f"Ошибка чтения SHP: {e}"}

def _read_qgis_project(path: str):
    # .qmd/.qgs это XML или текст
    return _read_text(path)

@tool
def load_data(path: str):
    """
    Загрузка файлов различных типов по их пути. 
    Инструмент автоматически определяет тип данных по расширению файла
    и возвращает структуру, удобную для анализа агентом.

    Назначение:
        Используется, когда в базе данных хранятся пути к разным типам файлов.
        Агент вызывает load_data(path), чтобы получить содержимое или метаданные.

    Как работает:
        Файл ОБЯЗАТЕЛЬНО должен существовать по указанному пути.
        Инструмент НЕ возвращает бинарные данные — только текст, словари 
        или метаданные, которые безопасны для LLM.

    Поддерживаемые форматы и поведение:

    1. Текстовые файлы:
        - .txt, .md, .prj, .cpj — возвращаются как строка.
        - .csv — возвращается как список строк (list[list[str]]).
        - .json — возвращается как dict.

    2. Георастр (TIFF):
        - .tif, .tiff
        - возвращаются ТОЛЬКО метаданные:
          { "width": ..., "height": ..., "crs": ..., "bounds": ..., ... }
        - піксели и бинарные данные НЕ возвращаются.

    3. Векторные данные (Shapefile):
        - .shp
        - возвращаются геометрии и атрибуты в формате GeoJSON:
          { "type": "FeatureCollection", "features": [...] }
        - файлы .shx, .dbf, .prj подтягиваются автоматически.

    4. Проекты QGIS:
        - .qmd, .qgs
        - возвращаются как текст.

    Формат возвращаемого результата:
        Всегда dict:
        {
            "type": <тип_данных>,
            "content": <содержимое или метаданные>
        }

    Ограничения:
        - Агент должен передавать корректный путь.
        - Инструмент не обрабатывает изображения, PDF, ZIP и бинарные форматы.
        - При ошибке возвращается:
            { "error": "описание ошибки" }

    Пример использования:
        1. Получить путь через SQL.
        2. Вызвать:
            load_data("S:/data/reports/area_5_2024.txt")

    Агенту:
        Используй этот инструмент, когда нужно открыть файл или получить его метаданные,
        а путь к файлу был получен из базы данных или предоставлен пользователем.
    """
    if not os.path.exists(path):
        return {"error": f"Файл не найден: {path}"}

    ext = os.path.splitext(path)[1].lower()

    if ext in [".txt", ".prj", ".cpj", ".md"]:
        return {"type": "text", "content": _read_text(path)}

    if ext == ".json":
        return {"type": "json", "content": _read_json(path)}

    if ext == ".csv":
        return {"type": "csv", "content": _read_csv(path)}

    if ext in [".tif", ".tiff"]:
        return {"type": "tiff_metadata", "content": _read_tiff_metadata(path)}

    if ext == ".shp":
        return {"type": "shapefile", "content": _read_shapefile(path)}

    if ext in [".qmd", ".qgs"]:
        return {"type": "qgis_project", "content": _read_qgis_project(path)}

    return {"error": f"Формат файла не поддерживается: {ext}"}    
       
