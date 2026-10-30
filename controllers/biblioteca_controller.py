from services import BibliotecaService


class BibliotecaController:
    
    def __init__(self, service: BibliotecaService) -> None:
        self._service: BibliotecaService = service
