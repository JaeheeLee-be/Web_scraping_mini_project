from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bookmark" DROP CONSTRAINT IF EXISTS "fk_bookmark_users_731523aa";
        ALTER TABLE "diary" ALTER COLUMN "title" TYPE VARCHAR(50) USING "title"::VARCHAR(50);
        ALTER TABLE "bookmarks" RENAME TO "bookmark";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_bookmark_user_id_46416a" ON "bookmark" ("user_id", "quote_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_bookmark_user_id_46416a";
        ALTER TABLE "diary" ALTER COLUMN "title" TYPE VARCHAR(255) USING "title"::VARCHAR(255);
        ALTER TABLE "bookmark" RENAME TO "bookmarks";
        ALTER TABLE "bookmark" ADD CONSTRAINT "fk_bookmark_users_731523aa" FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;"""


MODELS_STATE = (
    "eJztWl1P2zAU/StVn5jEJuhgQ3srUDa20Q7IPjSEIjcxrdXELrYzqCb++2znO02ypLQsHn"
    "lLr+91fE+ce45v87vrEhs67JVBZhAfOsCaOYjx7rvO7y4GLhQXBR7bnS6Yz+NxaeBg7KgQ"
    "Ln3Nccp5zDgFlpz6BjgMCpMNmUXRnCOChRV7jiONxBKOCE9ik4fRrQdNTiaQTyEVA1fXwo"
    "ywDe8hC3/OZ+YNgo6dWjuy5b2V3eSLubKdYn6iHOXdxqZFHM/FsfN8wacER94Iq+VPIIYU"
    "cCin59STy5erCxIOM/JXGrv4S0zE2PAGeA5PpFsRA4tgiZ9YDVMJTuRdXvZ2997uHbx+s3"
    "cgXNRKIsvbBz+9OHc/UCEwNLoPahxw4HsoGGPc1ANchu5oCmg+dlFABj6x6Cx8IVj/FD8X"
    "3JsOxBM+laDt75eg9a1/cfShf7ElvF7IXIjYxv42HwZDPX9MQhpDCO/niELbBHwZx2MBBU"
    "cuzMcyHZkB1A5CX4UXq8AbGmJ843dyPQCX4Gmcng0ujf7ZF7lyl7FbR0HSNwZypKesi4x1"
    "600G+miSzvdT40NH/uz8HA0HCjHC+ISqO8Z+xs+uXBPwODExuTOBnUw7NIem1JP0GKRmrU"
    "qSiPh7OWnGA1tHRZFl+GaWW1AkIssAnhAK0QR/gguF46lYEcAWzMEtIKGvwTTNw+8h3AOh"
    "NS5aFNxF1JTcGiI9kRTkfmntXx71jwddBeJYEOcdoLaZQlOOkB7JWCLf5SG352YtAIOJyl"
    "9mIdecBDaH9UPAi7leJsRahteN4TGyZuq6BsknY3Tk+f2dCjS/v1PI8nIoQ/IuQE4dCKMA"
    "HfHbiE6yKJQJr6CT0pF66qSuyMEeYWcRPDtNdFOwzUpl0xwwdkcEMU0Bm9Z5R5YCV3pXgi"
    "U+5bNMvSy7vYMKL4vwKnxZ1FiOqipWCJkDXPoEnob/MJjg5NMFdIBKtVB1LR/9m/ciFemv"
    "1Ja0EaAIssehcSwmWWgMglKgYkVMzv5ILKQ8PA+m0gySTappf4vkyOlo7xTraTtyafW0Rn"
    "qaI+7UEtNRwHqU4FPT2/q1tLgdhziHqgx4X7D/EiG6oFgm8AY/jJS2C9HaOuv/eJHSd59H"
    "w/ehewLdo8+jw1ZePw953XYl267k/96VPCRk5gI6y5NS0VipmhonvdYqqK6SoN16hEN5fd"
    "3qrM3qrLbsVQYxBi3antVRS4Y8J9hK2EJBsga6OA/naR6CVfkiuTuaRBg+tDlsEWFeTBUq"
    "p/afLO0YoT03buLcKM4eU5IjjosbGnGELphu6N+tlRr2oVB9ZEM2qYqbB/g/acZG/elcWo"
    "h712XMkGiWt+SgEzmEj87kggzqUMRSoC5F7SmIYqUK1/7vtPFSl4Kl4GuuaiVv+WG1dU/L"
    "ulfz0J+Kek7n/ra1vgJobWt9Da31dKMuLs6P7jLpSI9Z9DIVqUm9pj6kyJrm0WwwUkqwIP"
    "ZpibVhZa2MWH9BynJf0OLGSCJEl0PEE3z3K1+NGiAG7noCuLtT5WsZ4VX8LehO9e9lPl6O"
    "hnX7nl+xSPDKRhbf7siPPK+bCWsJijLr8sNt9hy7nf4mQ05Q83C7fnp5+AO1ajIC"
)
