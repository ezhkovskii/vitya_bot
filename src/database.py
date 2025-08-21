
# from config import DB_PATH

# db: aiosqlite.Connection | None = None

# async def open_db():
#     global db
#     db = await aiosqlite.connect(DB_PATH)
#     db.row_factory = aiosqlite.Row
#     await db.execute("PRAGMA foreign_keys = ON;")
#     await db.execute("PRAGMA journal_mode = WAL;")
#     await db.execute("PRAGMA synchronous = NORMAL;")
#     await db.execute(
#         """
#         CREATE TABLE IF NOT EXISTS chats (
#             chat_id INTEGER PRIMARY KEY,
#             title TEXT,
#             created_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
#             deleted_at INTEGER
#         )
#         """
#     )
#     await db.execute(
#         """
#         CREATE TABLE IF NOT EXISTS users (
#             user_id INTEGER PRIMARY KEY,
#             username TEXT,
#             first_name TEXT,
#             last_name TEXT,
#             created_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
#             deleted_at INTEGER
#         )
#         """
#     )
#     await db.executescript(
#         """
#         CREATE TABLE IF NOT EXISTS user_chats (
#             user_id INTEGER NOT NULL,
#             chat_id INTEGER NOT NULL,
#             created_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
#             deleted_at INTEGER,
#             PRIMARY KEY (user_id, chat_id),
#             FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
#             FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
#         );

#         CREATE INDEX IF NOT EXISTS idx_user_chats_chat_id ON user_chats(chat_id);
#         """
#     )
#     await db.commit()

# async def close_db():
#     if db is not None:
#         await db.close()

# async def get_db():
#     global db
#     if db is None:
#         raise RuntimeError("Database is not initialized. Call open_db() at startup.")
#     return db

# async def init_db():
#     await open_db()

# async def add_chat(chat_id: int, title: str, connection: aiosqlite.Connection | None = None):
#     conn = connection or await get_db()
#     await conn.execute(
#         """
#         INSERT INTO chats (chat_id, title)
#         VALUES (?, ?)
#         ON CONFLICT(chat_id) DO UPDATE SET
#             deleted_at = NULL
#         """,
#         (chat_id, title),
#     )
#     await conn.commit()

# async def add_user(
#     user_id: int,
#     chat_id: int,
#     username: str | None,
#     first_name: str,
#     last_name: str | None,
#     connection: aiosqlite.Connection | None = None
# ):
#     conn = connection or await get_db()
#     # Upsert user
#     await conn.execute(
#         """
#         INSERT INTO users (user_id, username, first_name, last_name)
#         VALUES (?, ?, ?, ?)
#         ON CONFLICT(user_id) DO UPDATE SET
#             username = excluded.username,
#             first_name = excluded.first_name,
#             last_name = excluded.last_name
#         """,
#         (user_id, username, first_name, last_name),
#     )
#     await conn.execute(
#         """
#         INSERT INTO user_chats (user_id, chat_id) VALUES (?, ?) ON CONFLICT(user_id, chat_id) DO UPDATE SET
#         deleted_at = NULL
#         """,
#         (user_id, chat_id),
#     )
#     await conn.commit()

# async def get_users_from_chat(chat_id: int, connection: aiosqlite.Connection | None = None):
#     conn = connection or await get_db()
#     cursor = await conn.execute(
#         """
#         SELECT u.user_id, u.username
#         FROM user_chats uc
#         JOIN users u ON u.user_id = uc.user_id
#         WHERE uc.chat_id = ? and uc.deleted_at is null
#         """,
#         (chat_id,),
#     )
#     return await cursor.fetchall()

# async def remove_user(user_id: int, chat_id: int, connection: aiosqlite.Connection | None = None):
#     conn = connection or await get_db()
#     await conn.execute(
#         "UPDATE user_chats SET deleted_at = strftime('%s','now') WHERE chat_id = ? AND user_id = ?",
#         (chat_id, user_id),
#     )
#     await conn.commit()


# async def delete_chat(chat_id: int, connection: aiosqlite.Connection | None = None):
#     """Soft-delete a chat by setting deleted_at to current UTC epoch seconds."""
#     conn = connection or await get_db()
#     await conn.execute(
#         "UPDATE chats SET deleted_at = strftime('%s','now') WHERE chat_id = ?",
#         (chat_id,),
#     )
#     await conn.commit()


# async def exists_user_in_chat(user_id: int, chat_id: int, connection: aiosqlite.Connection | None = None) -> bool:
#     """Return True if a user currently belongs to a chat (not soft-deleted)."""
#     conn = connection or await get_db()
#     cursor = await conn.execute(
#         "SELECT 1 FROM user_chats WHERE user_id = ? AND chat_id = ? AND deleted_at IS NULL LIMIT 1",
#         (user_id, chat_id),
#     )
#     row = await cursor.fetchone()
#     return row is not None
