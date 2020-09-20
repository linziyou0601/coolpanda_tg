CONFIG = {
    "DB_HOST": "127.0.0.1",
    "DB_USER": "root",
    "DB_PASSWORD": "Mm552288369@",
    "DB_DATABASE": "coolpanda",

    "DB_CREATE_TABLE": '''
    CREATE TABLE IF NOT EXISTS tg_user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        channel_id TEXT NOT NULL COMMENT "頻道 ID",
        mute TINYINT DEFAULT 0 COMMENT "0=可以聊天, 1=安靜",
        global_talk TINYINT DEFAULT 1 COMMENT "0=這裡教的話, 1=所有人教的話",
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tg_replied (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type TEXT NOT NULL COMMENT "訊息種類",
        message TEXT NOT NULL COMMENT "訊息內容",
        valid TINYINT NOT NULL COMMENT "0=功能型, 1=關鍵字, 2=一般型",
        channel_pk INT NOT NULL COMMENT "發送至頻道 ID",
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tg_received (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type TEXT NOT NULL COMMENT "訊息種類",
        message TEXT NOT NULL COMMENT "訊息內容",
        channel_pk INT NOT NULL COMMENT "發送者頻道 ID",
        user_pk INT NOT NULL COMMENT "發送者 ID",
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tg_pushed (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type TEXT NOT NULL COMMENT "訊息種類",
        title TEXT NOT NULL COMMENT "訊息標題",
        message TEXT NOT NULL COMMENT "訊息內容",
        channel_id TEXT NOT NULL COMMENT "發送至頻道 ID",
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tg_postfix (
        id INT AUTO_INCREMENT PRIMARY KEY,
        start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "啟始日期",
        last_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT "結束日期",
        content TEXT NOT NULL COMMENT "後綴內容",
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    '''
}

# INSERT INTO tg_user (id, channel_id) VALUES (0, "autoLearn");
# UPDATE tg_user SET id = '0' WHERE tg_user.channel_id = "autoLearn";

def ENV(key, default=None):
    return CONFIG.get(key, default)