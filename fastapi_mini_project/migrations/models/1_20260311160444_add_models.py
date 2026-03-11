from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "token_blacklist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(255) NOT NULL UNIQUE,
    "expired_at" TIMESTAMPTZ NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "diary" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "quotes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "author" VARCHAR(255) NOT NULL
);
        CREATE TABLE IF NOT EXISTS "bookmarks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "quote_id" INT NOT NULL REFERENCES "quotes" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "questions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "question_text" TEXT NOT NULL
);
        CREATE TABLE IF NOT EXISTS "user_questions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "question_id" INT NOT NULL REFERENCES "questions" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        ALTER TABLE "users" ADD "password_hash" VARCHAR(128);
        ALTER TABLE "users" RENAME COLUMN "username" TO "nickname";
        ALTER TABLE "users" ALTER COLUMN "email" TYPE VARCHAR(255) USING "email"::VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" RENAME COLUMN "nickname" TO "username";
        ALTER TABLE "users" DROP COLUMN "password_hash";
        ALTER TABLE "users" ALTER COLUMN "email" TYPE VARCHAR(100) USING "email"::VARCHAR(100);
        DROP TABLE IF EXISTS "diary";
        DROP TABLE IF EXISTS "token_blacklist";
        DROP TABLE IF EXISTS "bookmarks";
        DROP TABLE IF EXISTS "quotes";
        DROP TABLE IF EXISTS "user_questions";
        DROP TABLE IF EXISTS "questions";"""


MODELS_STATE = (
    "eJztW21P2zAQ/itVPzGJTdDBhvatQNnYRjsgbAiEIjcxrdXELrYzqCb++2zn/XVNaaEe+d"
    "ae7xzfY/ueu2v6p+0SGzrsnUEmEO87wJo4iPH2p9afNgYuFB9KNDZbbTCdxuNSwMHQUSZc"
    "6prDlPKQcQosOfUtcBgUIhsyi6IpRwQLKfYcRwqJJRQRHsUiD6M7D5qcjCAfQyoGrm+EGG"
    "EbPkAWfp1OzFsEHTu1dmTLZyu5yWdTJTvG/EgpyqcNTYs4notj5emMjwmOtBFWyx9BDCng"
    "UE7PqSeXL1cXOBx65K80VvGXmLCx4S3wHJ5wd04MLIIlfmI1TDk4kk9529ne+biz9/7Dzp"
    "5QUSuJJB8fffdi331DhUDfaD+qccCBr6FgjHFTG5iH7mAMaDF2kUEGPrHoLHwhWC+Knwse"
    "TAfiER9L0HZ3K9D62T07+NI92xBab6QvRBxj/5j3g6GOPyYhjSGED1NEoW0CnsfxUEDBkQ"
    "uLsUxbZgC1A9N34YdF4A0FMb7xnVwOwBV4GscnvXOje/JDrtxl7M5RkHSNnhzpKOksI934"
    "kIE+mqT169j40pJfW1eDfk8hRhgfUfXEWM+4ass1AY8TE5N7E9hJt0NxKErtpMcgNWtFko"
    "TFv8PJemzYMiKKDMO3k8KAIhHJA3hEKEQj/A3OFI7HYkUAW7AAt4CELoJp1g+/x/AMhNI4"
    "aFFwH1FT8mgI94RTkPuhtXt+0D3stRWIQ0Gc94DaZgpNOUI6JCOJdPNDbsfNSgAGI+W/9E"
    "KuOQlsAeuHgJdzvXSINQyvG8NjZE3U5xokn7TRked3t+ag+d2tUpaXQxmSdwFy6kAYGeiI"
    "30ryJItC6fACeVLaUs88qS18sAfYmQV7p0neFByzyrRpChi7J4KYxoCN69yRnOFCdyVY4n"
    "PuZeqybHf25rgsQqv0sqixgqyqPEPIFHDpCjwN/34wwdG3M+gA5Wpp1pUv/dfvIpXlX6kj"
    "aSNAEWRPQ+NQTDLTGIQhIRMX0MkTYdgPptEYCZWLixUxOfsT4ZCJ8mkwlWaQrLKu8C9LQW"
    "ER3aLyysKOVJrKYpk0tereIeJOrbIiMlhOTvzcRL+arJhgDnEBbxvwoeQIJkx0AbIq2+1d"
    "GqlEN4Rr46R7+SaV7H4f9D+H6gl4D74P9pta43XUGk2LtmnR/u8t2ijhLsimksl4eUKVyv"
    "ybpGrd7mZVUnXnEQ7rRbikyWsKcQ0vNLzwMryQPHnq9i0BttNwHn1xSwaidSJUH9oCNo0w"
    "L6dS5VPDo9rxaFNXr6KuFrXZmBSQRHnPJ7bQBdMVNX0W+nXndbfwV8sJQQu/kBbi9n4VMy"
    "R+T2jIQSdyCLfO5IIM6lBEzlCXoPYcRLFQhGt+mlt5qEvBUvLq33whL79ZTdzTMu7V7C+l"
    "rF5Tt6RpMS0AWtNiWnqLKQ7OT+4y6UiPWfQyEWmdek1dSJE1LqLZYKSSYEGs0xDrmoW1Km"
    "L9DSkrvKDljZGEiS5FxDO8DiOvRg0QA3U9AdzemudvCkKr/MXhrdwfFUr7nl/PB/26fc8L"
    "LBy8tpHFN1vyjeCb9YS1AkXpdXVxm61jN9PvrMgJaha3y6eXx78Z0+wb"
)
