from api.views_set.lib import *
from api.functions.qa_helper import QAHelper


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def question_create(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    anonymous = req_data['anonymous']
    classroom_uuid = req_data['classroom_uuid']
    content = req_data['content']
    qa_helper = QAHelper(user_id, role, anonymous=anonymous)
    qa_helper.create_question(classroom_uuid, content)
    res_data = dict(
        error=0,
        timestamp=qa_helper.timestamp_now
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def question_close(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    question_uuid = req_data['question_uuid']
    role = req_data['role']
    qa_helper = QAHelper(user_id, role)
    success = qa_helper.close_question(question_uuid)
    res_data = dict(
        success=success
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def question_get_list(request):
    user_id = request.user.username
    role = request.GET['role']
    school_uuid = request.GET['school_uuid']
    page_number = request.GET['page_number']
    filter_type = request.GET['filter_type']
    page_number = int(page_number)
    qa_helper = QAHelper(user_id, role)
    questions = qa_helper.get_question_list(filter_type, page_number, school_uuid)
    res_data = dict(
        error=0,
        questions=questions
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def answer_create(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    anonymous = req_data['anonymous']
    question_uuid = req_data['question_uuid']
    classroom_uuid = req_data['classroom_uuid']
    content = req_data['content']
    qa_helper = QAHelper(user_id, role, anonymous=anonymous)
    qa_helper.create_answer(question_uuid, classroom_uuid, content)
    res_data = dict(
        error=0,
        timestamp=qa_helper.timestamp_now
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def answer_agree(request):
    user_id = request.user.username
    req_data = json.loads(request.body)
    role = req_data['role']
    answer_uuid = req_data['answer_uuid']
    agree = req_data['agree']
    qa_helper = QAHelper(user_id, role)
    if agree:
        qa_helper.agree_answer(answer_uuid)
    else:
        qa_helper.disagree_answer(answer_uuid)
    res_data = dict(
        error=0
    )
    return Response(data=res_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def answer_get_list(request):
    user_id = request.user.username
    role = request.GET['role']
    question_uuid = request.GET['question_uuid']
    page_number = request.GET['page_number']
    page_number = int(page_number)
    qa_helper = QAHelper(user_id, role)
    answers = qa_helper.get_answer_list(question_uuid, page_number)
    res_data = dict(
        error=0,
        answers=answers
    )
    return Response(data=res_data, status=status.HTTP_200_OK)