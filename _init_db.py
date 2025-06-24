import aiosqlite
import asyncio

async def init_db():
    async with aiosqlite.connect("omikuji.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS omikuji (
                accoutId INTEGER,
                result TEXT,
                roomId INTEGER,
                name TEXT,
                date NUMERIC
            )
        """)
        await db.commit()
        print("おみくじテーブル作成完了")

if __name__ == "__main__":
    asyncio.run(init_db())
