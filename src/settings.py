from pathlib import Path
from typing import Any


class Config:
    """
    Configurações principais do projeto.
    """

    # Diretórios base
    BASE_DIR: Path = Path.cwd()
    DIR_RAW: Path = BASE_DIR / "data" / "raw"
    DIR_PROCESSED: Path = BASE_DIR / "data" / "processed"

    # URL da fonte dos dados
    FILE_URL: str = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"

    # Nomes de arquivos
    INTERNAL_EXCEL_NAME: str = "Online Retail.xlsx"
    NEW_FILENAME: str = "retail_data"
    FILE_NAME: str = "retail_data.parquet"
    TEMP_ZIP_NAME: str = "temp_download.zip"

    @property
    def FILE_ZIP(self) -> Path:
        """Caminho completo para o arquivo zip temporário."""
        return self.DIR_RAW / self.TEMP_ZIP_NAME

    @property
    def FILE_INPUT(self) -> Path:
        """Caminho completo para o arquivo de entrada (excel)."""
        return self.DIR_RAW / self.INTERNAL_EXCEL_NAME

    @property
    def FILE_OUTPUT(self) -> Path:
        """Caminho completo para o arquivo de saída (parquet)."""
        return self.DIR_PROCESSED / self.FILE_NAME


# Instância padrão de configuração
config = Config()
