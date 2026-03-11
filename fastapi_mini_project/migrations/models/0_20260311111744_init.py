from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztlm9vmzAQxr8K4lUmdVXKkrbaO5plaqYlmVq6Ta0q5IADVoxNwayNqnz3+gzEQP4omb"
    "p1kfYOnnsO3/0gd3k2I+5jmh7fpDgxPxrPJkMRlhc1/cgwURxrFQSBJlQZM+lQCpqkIkGe"
    "kOIU0RRLycepl5BYEM6kyjJKQeSeNBIWaClj5CHDruABFqEq5O5eyoT5+Amn5W08c6cEU7"
    "9WJ/HhbKW7Yh4rbcDEZ2WE0yaux2kWMW2O5yLkbOkmTIAaYIYTJDA8XiQZlA/VFW2WHeWV"
    "akteYiXHx1OUUVFpd0cGHmfAT1aTqgYDOOW9ddI565x/OO2cS4uqZKmcLfL2dO95oiIwcs"
    "yFiiOBcofCqLnBa1PXK/R6IUrW46vmNCDK0psQS2RvSjFCTy7FLBChvO22tyD7bl/1Lu2r"
    "Vrf9Djrh8lPOP/BREbFUCKhqijhChO6DcJlwiPxO2rsAlK6NBFWsjtBLMDTsIrHK8ZOMCB"
    "Lh9SzrmQ2gfpF6XF78Dt5S0Hz1ZHslwLIHf8zovHh3W/g6g2H/2rGH36CTKE0fqEJkO32I"
    "WEqdN9TWaeNVLB9i/Bg4lwbcGrfjUV8R5KkIEnWi9jm3JtSEMsFdxh9d5Fc+s1ItwSxgTE"
    "9nlYEDwgR5s0eU+O5KhFt8k3c1FFlRU0EMBeq1AFwos9haNk6IF67bZ0Vk60ZD2vN/pR3Q"
    "Svsl/4hASXuM40rK6wzkvzAxaiPZ6nZ3GMnStXEkq1h9JMNPYw+Ihf0wAf6ZncaZwGzNQv"
    "tyPR5tWGY6pQHyhskG73ziiSODklTc/5tYt1CErmtLq4TXGto/m1x7X8cXzW0ED7iQjN90"
    "vSxeALL0MlU="
)
