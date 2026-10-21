import requests
import json

r = requests.post('http://127.0.0.1:5000/api/v1/auth/login', json={'email':'student@demo.com','password':'Demo@1234'})
token = r.json()['access_token']
headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

# First get the attempt ID by starting the assessment
r = requests.post('http://127.0.0.1:5000/api/v1/assessments/13/start', headers=headers)
result = r.json()
attempt_id = result['attempt']['id']
questions = result['questions']
print('Attempt ID:', attempt_id)

# Submit answers for communication scenarios
body = {
    'answers': [
        {
            'question_id': questions[0]['id'],
            'answer_text': 'I would approach this calmly by first acknowledging their perspective, then presenting my concerns with specific technical evidence about the security vulnerabilities. I would use data from security audits and reference industry best practices. The goal is to make it about the code, not the person, and propose alternative solutions that address the same requirements securely.'
        },
        {
            'question_id': questions[1]['id'],
            'answer_text': 'I would prepare a clear business case showing the cost of bugs vs. refactoring investment. I would present metrics on current bug frequency, customer impact, and development velocity loss. Then propose a phased refactoring plan with measurable milestones and risk mitigation. This shows I understand both technical and business priorities.'
        },
        {
            'question_id': questions[2]['id'],
            'answer_text': 'First, I would acknowledge the issue immediately and apologize to the client. Then I would explain what happened transparently, what we are doing to fix it right now, and our plan to prevent recurrence. I would set up a follow-up meeting with a detailed post-mortem and action items. The key is owning the mistake and showing concrete improvement steps.'
        }
    ]
}
r = requests.post('http://127.0.0.1:5000/api/v1/assessments/' + str(attempt_id) + '/submit', json=body, headers=headers)
result = r.json()
print('Submit status:', r.status_code)
print('Score:', result['score'])
print('Message:', result['message'])