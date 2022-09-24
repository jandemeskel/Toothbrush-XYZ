FROM public.ecr.aws/lambda/python:3.8

COPY requirement.txt .

RUN pip3 install -r requirement.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["manipulation_script.handler"] 