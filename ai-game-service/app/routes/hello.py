from fastapi import APIRouter

router = APIRouter(prefix='/print')

@router.get('/hello')
def print_hello():
    return {'mesg':'Hell yeahhh!'}