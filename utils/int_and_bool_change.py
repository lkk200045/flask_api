
class TypeChange:
    
    def get_type(type):
        if type.lower() == 'false':
            return 0
        elif type.lower() == 'true':
            return 1
        elif type == 0:
            return 'false'
        elif type == 1:
            return 'true'
        else:
            return "TypeError"