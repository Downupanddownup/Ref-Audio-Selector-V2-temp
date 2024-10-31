import sqlite3


def init_master_table(db_path):
    # 连接到SQLite数据库，如果不存在则创建
    conn = sqlite3.connect(db_path)

    # 创建一个游标对象用于执行SQL命令
    cursor = conn.cursor()

    # 音色融合
    cursor.execute('''
        CREATE TABLE tab_obj_sound_fusion_audio (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- 自增编号
            RoleName TEXT DEFAULT '' COMMENT '角色名称',
            AudioName TEXT DEFAULT '' COMMENT '音频名称',
            AudioPath TEXT DEFAULT '' COMMENT '音频路径',
            Content TEXT DEFAULT '' COMMENT '音频内容',
            Language TEXT DEFAULT '' COMMENT '音频语种',
            Category TEXT DEFAULT '' COMMENT '音频分类',
            AudioLength INTEGER DEFAULT 0 COMMENT '音频时长',
            Remark TEXT DEFAULT '' COMMENT '备注',
            CreateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- 创建时间
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_obj_inference_text (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用INTEGER PRIMARY KEY AUTOINCREMENT来实现自增功能
            Category TEXT, -- 分类
            TextContent TEXT, -- 文本
            TextLanguage TEXT, -- 语种
            CreateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- SQLite中默认的时间戳格式
        );
    ''')

    # 创建一个新表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tab_sys_cache (
            Id INTEGER PRIMARY KEY AUTOINCREMENT, -- SQLite使用INTEGER PRIMARY KEY AUTOINCREMENT来实现自增功能
            Type TEXT, -- 类型
            KeyName TEXT, -- 文本
            Value TEXT, -- 语种
            CreateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- SQLite中默认的时间戳格式
        );
    ''')

    # 提交事务（如果没有这一步，则不会保存更改）
    conn.commit()

    # 关闭连接
    conn.close()
