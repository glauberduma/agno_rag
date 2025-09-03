try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False

from pathlib import Path
from typing import List, Optional, Dict, Any
from agno.document import Document
from agno.document.reader.text_reader import TextReader
from agno.utils.log import logger


class EnhancedTextReader(TextReader):
    """
    Enhanced TextReader que detecta automaticamente o encoding dos arquivos
    e suporta múltiplos encodings comuns.
    """
    
    def __init__(
        self,
        chunk: bool = True,
        chunk_size: int = 5000,
        chunking_strategy: Optional[Any] = None,
        fallback_encodings: List[str] = None
    ):
        super().__init__(chunk=chunk, chunk_size=chunk_size, chunking_strategy=chunking_strategy)
        
        # Lista de encodings para tentar como fallback
        self.fallback_encodings = fallback_encodings or [
            'utf-8',
            'latin-1',
            'iso-8859-1', 
            'cp1252',
            'windows-1252',
            'ascii'
        ]
    
    def detect_encoding(self, file_path: Path) -> str:
        """
        Detecta o encoding do arquivo usando chardet e fallbacks.
        """
        if HAS_CHARDET:
            try:
                # Primeiro, tenta detectar usando chardet
                with open(file_path, 'rb') as f:
                    raw_data = f.read(10000)  # Lê os primeiros 10KB para detecção
                
                detected = chardet.detect(raw_data)
                if detected and detected['encoding'] and detected['confidence'] > 0.7:
                    encoding = detected['encoding']
                    logger.debug(f"Encoding detectado para {file_path.name}: {encoding} (confiança: {detected['confidence']:.2f})")
                    return encoding
                
            except Exception as e:
                logger.debug(f"Erro na detecção automática de encoding para {file_path.name}: {e}")
        
        # Se a detecção falhar ou tiver baixa confiança, tenta os encodings de fallback
        for encoding in self.fallback_encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read(1000)  # Tenta ler os primeiros 1000 caracteres
                logger.debug(f"Encoding fallback bem-sucedido para {file_path.name}: {encoding}")
                return encoding
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"Erro ao testar encoding {encoding} para {file_path.name}: {e}")
                continue
        
        # Se nada funcionar, usa latin-1 como último recurso (sempre funciona)
        logger.warning(f"Usando latin-1 como último recurso para {file_path.name}")
        return 'latin-1'
    
    def read_file_with_encoding(self, file_path: Path) -> str:
        """
        Lê o arquivo usando o encoding detectado.
        """
        encoding = self.detect_encoding(file_path)
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            logger.debug(f"Arquivo {file_path.name} lido com sucesso usando encoding {encoding}")
            return content
        except Exception as e:
            logger.error(f"Erro ao ler arquivo {file_path.name} com encoding {encoding}: {e}")
            
            # Último recurso: tentar latin-1 com replace
            try:
                with open(file_path, 'r', encoding='latin-1', errors='replace') as f:
                    content = f.read()
                logger.warning(f"Arquivo {file_path.name} lido com latin-1 e errors='replace'")
                return content
            except Exception as e2:
                logger.error(f"Falha completa ao ler arquivo {file_path.name}: {e2}")
                raise
    
    def read(self, file: Path) -> List[Document]:
        """
        Lê um arquivo de texto detectando automaticamente o encoding.
        """
        try:
            content = self.read_file_with_encoding(file)
            
            # Se o conteúdo estiver vazio, retorna lista vazia
            if not content.strip():
                logger.warning(f"Arquivo {file.name} está vazio ou contém apenas espaços")
                return []
            
            # Cria documento(s) usando a lógica da classe pai
            if self.chunk:
                documents = []
                chunks = self.chunk_document(
                    Document(
                        content=content,
                        id=str(file),
                        name=file.name,
                        meta_data={
                            "file_path": str(file),
                            "file_name": file.name,
                            "file_size": file.stat().st_size
                        }
                    )
                )
                return chunks
            else:
                return [Document(
                    content=content,
                    id=str(file),
                    name=file.name,
                    meta_data={
                        "file_path": str(file),
                        "file_name": file.name,
                        "file_size": file.stat().st_size
                    }
                )]
                
        except Exception as e:
            logger.error(f"Erro ao processar arquivo {file}: {e}")
            return []
    
    async def async_read(self, file: Path) -> List[Document]:
        """
        Versão assíncrona da leitura (usa a versão síncrona internamente).
        """
        # Para simplicidade, usa a versão síncrona
        # Em uma implementação real, poderia usar aiofiles
        return self.read(file)
