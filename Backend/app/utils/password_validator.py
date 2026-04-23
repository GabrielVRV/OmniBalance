import re
from typing import List

class PasswordValidator:
    @staticmethod
    def validate_password(password: str) -> List[str]:
        """Valida a força da senha e retorna lista de erros"""
        errors = []
        
        # Mínimo 8 caracteres
        if len(password) < 8:
            errors.append("Senha deve ter pelo menos 8 caracteres")
        
        # Pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', password):
            errors.append("Senha deve conter pelo menos uma letra maiúscula")
        
        # Pelo menos uma letra minúscula
        if not re.search(r'[a-z]', password):
            errors.append("Senha deve conter pelo menos uma letra minúscula")
        
        # Pelo menos um número
        if not re.search(r'\d', password):
            errors.append("Senha deve conter pelo menos um número")
        
        # Pelo menos um caractere especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Senha deve conter pelo menos um caractere especial")
        
        # Não pode conter sequências comuns
        common_sequences = ['123456', 'abcdef', 'qwerty', 'password']
        for seq in common_sequences:
            if seq in password.lower():
                errors.append(f"Senha não pode conter sequências comuns como '{seq}'")
                break
        
        return errors
    
    @staticmethod
    def is_strong_password(password: str) -> bool:
        """Retorna True se a senha for forte"""
        return len(PasswordValidator.validate_password(password)) == 0
