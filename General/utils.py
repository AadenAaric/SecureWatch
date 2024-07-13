import bcrypt

def hash_user_id(user_id):
    # Convert user_id to string if necessary (depending on how it's passed)
    user_id_str = str(user_id)
    
    # Convert user_id to bytes using UTF-8 encoding
    user_id_bytes = user_id_str.encode('utf-8')
    
    # Generate salt and hash the user_id
    salt = bcrypt.gensalt()
    hashed_user_id = bcrypt.hashpw(user_id_bytes, salt)
    
    # Return the hashed user_id and the salt used (salt is embedded in the hashed_user_id)
    return hashed_user_id.decode('utf-8')

def verify_user_id(user_id, hashed_id):
    # Convert user_id to string if necessary (depending on how it's passed)
    user_id_str = str(user_id)
    
    # Convert user_id to bytes using UTF-8 encoding
    user_id_bytes = user_id_str.encode('utf-8')
    
    # Convert hashed_id to bytes
    hashed_id_bytes = hashed_id.encode('utf-8')
    
    # Verify the user_id against the hashed_id
    return bcrypt.checkpw(user_id_bytes, hashed_id_bytes)


