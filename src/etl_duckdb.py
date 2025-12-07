import duckdb
import requests
import zipfile
import os
from pathlib import Path
from config import (
    FILE_URL,
    FILE_ZIP,
    FILE_INPUT,
    FILE_OUTPUT,
    DIR_RAW,
    DIR_PROCESSED
)


def _setup_directories():
    """Cria a estrutura de pastas se não existir."""
    print(f"[SETUP] Verificando diretórios...")    
    DIR_RAW.mkdir(parents=True, exist_ok=True)
    DIR_PROCESSED.mkdir(parents=True, exist_ok=True)


def _download_file(url: str, file_dest: Path) -> bool:
    """Baixa o arquivo ZIP."""
    print(f"[EXTRACT] Baixando arquivo ZIP para: {file_dest}")
    
    try:
        res = requests.get(url, timeout=60, stream=True)
        res.raise_for_status()
        with open(file_dest, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Erro no download: {e}")
        return False


def _extract_zip(zip_path: Path, extract_to: Path):
    """Extrai o conteúdo do ZIP para a pasta raw."""
    print(f"[EXTRACT] Descompactando {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Arquivos extraídos em {extract_to}")
    except Exception as e:
        print(f"Erro ao descompactar: {e}")
        raise e


def _excel_to_parquet(input_path: Path, file_output: Path):
    """Usa a engine do DuckDB para converter Excel -> Parquet."""
    
    if not input_path.exists():
        print(f"[ERRO] Arquivo de entrada não encontrado: {input_path}")
        return

    print(f"[TRANSFORM] Convertendo Excel para Parquet via DuckDB...")

    try:
        conn = duckdb.connect()

        conn.install_extension("spatial")
        conn.load_extension("spatial")

        input_str = str(input_path).replace("\\", "/")
        output_str = str(file_output).replace("\\", "/")

        query = f"""
            COPY (
                SELECT * FROM st_read('{input_str}')
            ) TO '{output_str}' (FORMAT PARQUET, COMPRESSION 'SNAPPY');
        """

        conn.sql(query)
        print(f"[SUCESSO] Pipeline finalizado. Arquivo salvo em: {file_output}")
        
        count = conn.sql(f"SELECT count(*) FROM '{output_str}'").fetchone()[0]
        print(f"          Total de linhas processadas: {count}")

    except Exception as e:
        print(f"Erro ao converter excel para parquet: {e}")


def run_etl_pipeline():
    """
    Executa o pipeline ETL completo:
    1. Cria as pastas necessárias.
    2. Limpa a pasta raw.
    3. Faz o download do arquivo ZIP especificado por FILE_URL.
    4. Extrai o arquivo ZIP para o diretório de dados brutos.
    5. Converte o arquivo Excel extraído em formato Parquet usando DuckDB.
    6. Remove o arquivo ZIP após o processamento.
    """
    _setup_directories()
    
    if _download_file(FILE_URL, FILE_ZIP):
        _extract_zip(FILE_ZIP, DIR_RAW)
        _excel_to_parquet(FILE_INPUT, FILE_OUTPUT)
        if FILE_ZIP.exists():
            os.remove(FILE_ZIP)
    

if __name__ == "__main__":
    run_etl_pipeline()