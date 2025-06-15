"""
Model do Personagem (Player)
Representa um personagem do jogo com seus atributos e comportamentos
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from colorama import Fore


@dataclass
class Player:
    """
    Model que representa um personagem no banco de dados
    
    Attributes:
        id_jogador: ID único do personagem no banco
        nome: Nome do personagem
        vida_maxima: Vida máxima do personagem
        vida_atual: Vida atual do personagem
        forca: Força do personagem
        localizacao: Localização atual do personagem
        nivel: Nível do personagem
        experiencia: Experiência acumulada
    """
    id_jogador: Optional[int]
    nome: str
    vida_maxima: int
    vida_atual: int
    forca: int
    localizacao: str
    nivel: int
    experiencia: int
    
    def __post_init__(self):
        """Validações após inicialização"""
        if self.vida_atual > self.vida_maxima:
            self.vida_atual = self.vida_maxima
    
    def is_alive(self) -> bool:
        """Verifica se o personagem está vivo"""
        return self.vida_atual > 0
    
    def take_damage(self, damage: int) -> bool:
        """
        Aplica dano ao personagem
        
        Args:
            damage: Quantidade de dano a ser aplicado
            
        Returns:
            True se o personagem ainda está vivo após o dano
        """
        self.vida_atual = max(0, self.vida_atual - damage)
        return self.is_alive()
    
    def heal(self, amount: int) -> None:
        """
        Cura o personagem
        
        Args:
            amount: Quantidade de vida a ser restaurada
        """
        self.vida_atual = min(self.vida_maxima, self.vida_atual + amount)
    
    def gain_experience(self, amount: int) -> None:
        """
        Adiciona experiência ao personagem
        
        Args:
            amount: Quantidade de experiência a ser adicionada
        """
        self.experiencia += amount
    
    def level_up(self) -> bool:
        """
        Tenta fazer o personagem subir de nível
        
        Returns:
            True se subiu de nível
        """
        # Lógica simples: a cada 100 XP sobe de nível
        if self.experiencia >= self.nivel * 100:
            self.nivel += 1
            self.vida_maxima += 10
            self.vida_atual = self.vida_maxima  # Cura ao subir de nível
            self.forca += 2
            return True
        return False
    
    def get_health_percentage(self) -> float:
        """
        Retorna a porcentagem de vida atual
        
        Returns:
            Porcentagem de vida (0.0 a 1.0)
        """
        return self.vida_atual / self.vida_maxima if self.vida_maxima > 0 else 0.0
    
    def get_health_bar(self, width: int = 20) -> str:
        """
        Retorna uma barra de vida visual
        
        Args:
            width: Largura da barra em caracteres
            
        Returns:
            String representando a barra de vida
        """
        percentage = self.get_health_percentage()
        filled = int(width * percentage)
        empty = width - filled
        
        if percentage > 0.6:
            color = Fore.GREEN
        elif percentage > 0.3:
            color = Fore.YELLOW
        else:
            color = Fore.RED
            
        bar = "█" * filled + "░" * empty
        return f"{color}{bar}{Fore.RESET}"
    
    def __str__(self) -> str:
        """Representação string do personagem"""
        return f"Player(id={self.id_jogador}, nome='{self.nome}', vida={self.vida_atual}/{self.vida_maxima})"
    
    def __repr__(self) -> str:
        """Representação detalhada do personagem"""
        return (f"Player(id_jogador={self.id_jogador}, nome='{self.nome}', "
                f"vida_maxima={self.vida_maxima}, vida_atual={self.vida_atual}, "
                f"forca={self.forca}, localizacao='{self.localizacao}', "
                f"nivel={self.nivel}, experiencia={self.experiencia})")
    
    def __eq__(self, other) -> bool:
        """Comparação de igualdade baseada no ID"""
        if not isinstance(other, Player):
            return False
        return self.id_jogador == other.id_jogador
    
    def __hash__(self) -> int:
        """Hash baseado no ID"""
        return hash(self.id_jogador)


@dataclass
class PlayerSession:
    """
    Model que representa um personagem ativo na sessão do jogo
    
    Attributes:
        id_jogador: ID único do personagem no banco
        nome: Nome do personagem
        vida_max: Vida máxima do personagem
        vida_atual: Vida atual do personagem
        xp: Experiência acumulada
        forca: Força do personagem
        id_chunk_atual: ID do chunk onde o personagem está
        chunk_bioma: Nome do bioma atual (cache para performance)
        chunk_mapa_nome: Nome do mapa atual (cache para performance)
        chunk_mapa_turno: Turno atual (Dia/Noite) (cache para performance)
    """
    id_jogador: int
    nome: str
    vida_max: int
    vida_atual: int
    xp: int
    forca: int
    id_chunk_atual: Optional[int] = None
    chunk_bioma: Optional[str] = None
    chunk_mapa_nome: Optional[str] = None
    chunk_mapa_turno: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o personagem para dicionário"""
        return {
            'id_jogador': self.id_jogador,
            'nome': self.nome,
            'vida_max': self.vida_max,
            'vida_atual': self.vida_atual,
            'xp': self.xp,
            'forca': self.forca,
            'id_chunk_atual': self.id_chunk_atual,
            'chunk_bioma': self.chunk_bioma,
            'chunk_mapa_nome': self.chunk_mapa_nome,
            'chunk_mapa_turno': self.chunk_mapa_turno
        }
    
    def is_alive(self) -> bool:
        """Verifica se o personagem está vivo"""
        return self.vida_atual > 0
    
    def take_damage(self, damage: int) -> bool:
        """
        Aplica dano ao personagem
        
        Args:
            damage: Quantidade de dano a ser aplicado
            
        Returns:
            True se o personagem ainda está vivo após o dano
        """
        self.vida_atual = max(0, self.vida_atual - damage)
        return self.is_alive()
    
    def heal(self, amount: int) -> None:
        """
        Cura o personagem
        
        Args:
            amount: Quantidade de vida a ser restaurada
        """
        self.vida_atual = min(self.vida_max, self.vida_atual + amount)
    
    def gain_xp(self, amount: int) -> None:
        """
        Adiciona experiência ao personagem
        
        Args:
            amount: Quantidade de XP a ser adicionada
        """
        self.xp += amount

    def get_location_display(self) -> str:
        """
        Retorna a localização formatada para exibição
        
        Returns:
            String formatada da localização
        """
        if self.chunk_bioma:
            return f"{self.chunk_bioma} ({self.chunk_mapa_nome} - {self.chunk_mapa_turno})"
        return "Desconhecida"
    
    def get_health_percentage(self) -> float:
        """
        Retorna a porcentagem de vida atual
        
        Returns:
            Porcentagem de vida (0.0 a 1.0)
        """
        return self.vida_atual / self.vida_max if self.vida_max > 0 else 0.0
    
    def get_health_bar(self, width: int = 20) -> str:
        """
        Retorna uma barra de vida visual
        
        Args:
            width: Largura da barra em caracteres
            
        Returns:
            String representando a barra de vida
        """
        percentage = self.get_health_percentage()
        filled = int(width * percentage)
        empty = width - filled
        
        if percentage > 0.6:
            color = Fore.GREEN
        elif percentage > 0.3:
            color = Fore.YELLOW
        else:
            color = Fore.RED
            
        bar = "█" * filled + "░" * empty
        return f"{color}{bar}{Fore.RESET}"
    
    def can_move(self) -> bool:
        """
        Verifica se o personagem pode se mover
        
        Returns:
            True se pode se mover
        """
        return self.is_alive() and self.id_chunk_atual is not None
    
    def __str__(self) -> str:
        """Representação string do personagem"""
        return f"PlayerSession(id={self.id_jogador}, nome='{self.nome}', vida={self.vida_atual}/{self.vida_max})"
    
    def __repr__(self) -> str:
        """Representação detalhada do personagem"""
        return (f"PlayerSession(id_jogador={self.id_jogador}, nome='{self.nome}', "
                f"vida_max={self.vida_max}, vida_atual={self.vida_atual}, "
                f"xp={self.xp}, forca={self.forca}, "
                f"id_chunk_atual={self.id_chunk_atual})") 
