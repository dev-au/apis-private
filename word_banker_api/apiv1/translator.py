import jsonfrom fastapi import APIRouter, statusfrom pydantic import BaseModelfrom data.word_get import word_optionsfrom api_versions import api_v1from data.coder import get_api_limitfrom data.database import session, enginefrom data.models import Word, Keyfrom data.example import example_answerfrom fastapi.exceptions import HTTPExceptiontranslator_router = APIRouter(prefix='/get-word')session = session(bind=engine)class GetWord(BaseModel):    to_lang: str    text: str    api_key: str    class Config:        from_attributes = True        json_schema_extra = {            "example": {                "to_lang": "uz",                "text": "join",                "api_key": "example_api_key"            }        }@translator_router.post("/", tags=['Get words info'])async def root(info: GetWord):    text = info.text.lower()    api_key = info.api_key    if info.api_key == "example_api_key" and info.text == "join" and info.to_lang == "uz":        return example_answer    try:        default_limit = get_api_limit(api_key)        db_api = session.query(Key).filter(Key.api_key == info.api_key).first()        if db_api is None:            raise ValueError    except ValueError:        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,                             detail="This api key is invalid or already expired")    if default_limit == 7777:        api_limit = 0    else:        api_limit = db_api.api_limit        if api_limit == 0:            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,                                 detail="Your api key has run out of requests")        db_api.api_limit = api_limit - 1        session.commit()    if info.to_lang == "uz":        result = session.query(Word).filter(Word.word == text).first()        if result is None:            result = word_options(text, "uz")            if len(result['translates']) + len(result['definitions']) + len(result['synonyms']) + len(result['examples']):                new_word = Word(                    word=info.text,                    word_info=json.dumps(result)                )                session.add(new_word)                session.commit()        else:            result = json.loads(result.word_info)    else:        try:            result = word_options(text, info.to_lang)        except ValueError:            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,                                 detail="Invalid Destination language")    result['API-LIMIT'] = api_limit - 1    return HTTPException(status_code=status.HTTP_200_OK,                         detail="Success",                         headers=result)api_v1.include_router(translator_router)