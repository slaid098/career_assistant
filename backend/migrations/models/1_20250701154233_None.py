from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:  # noqa: ARG001
    return """
        CREATE TABLE IF NOT EXISTS "jobs" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "company" VARCHAR(255),
    "location" VARCHAR(255),
    "url" VARCHAR(512) NOT NULL UNIQUE,
    "description" TEXT,
    "salary" VARCHAR(255),
    "posted_date" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_jobs_url_54a18d" ON "jobs" ("url");
COMMENT ON TABLE "jobs" IS 'Model for storing job information in the database.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:  # noqa: ARG001
    return """
        """
