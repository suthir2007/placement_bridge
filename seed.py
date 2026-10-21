import sys
import warnings
warnings.filterwarnings("ignore")

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from app import create_app
from app.extensions import db, bcrypt
from app.models import (
    User, UserRole, StudentProfile, College, Skill, StudentSkill,
    Assessment, Question, Attempt, Answer, Company, RecruiterProfile, JobPosting, InternshipPosting,
    Application, ApplicationStatusHistory, TrainingProgram, TrainingEnrollment,
    PlacementDrive, Notification, StudentStage, Interview
)
from datetime import datetime, timedelta
import random

app = create_app()


def seed_db(app_instance=None):
    target_app = app_instance or app
    with target_app.app_context():
        print("🌱 Seeding PlacementPilot Database...")
        try:
            db.drop_all()
            db.create_all()

            pw_hash = bcrypt.generate_password_hash("Demo@1234").decode('utf-8')

            # 1. Colleges
            c1 = College(name="National Institute of Technology, Bengaluru", code="NITB", location="Bengaluru, KA")
            c2 = College(name="Indian Institute of Technology, Hyderabad", code="IITH", location="Hyderabad, TS")
            c3 = College(name="BITS Pilani, Goa Campus", code="BITSG", location="Goa, GA")
            db.session.add_all([c1, c2, c3])
            db.session.flush()

            # 2. Demo Users
            admin_user = User(email="admin@demo.com", password_hash=pw_hash, name="Dr. Rajesh Kumar (Admin)", role=UserRole.COLLEGE_ADMIN.value)
            student_user = User(email="student@demo.com", password_hash=pw_hash, name="Alex Johnson", role=UserRole.STUDENT.value)
            recruiter_user = User(email="recruiter@demo.com", password_hash=pw_hash, name="Sarah Jenkins", role=UserRole.INDUSTRY_RECRUITER.value)

            db.session.add_all([admin_user, student_user, recruiter_user])
            db.session.flush()

            # Demo Profiles
            demo_student_profile = StudentProfile(
                user_id=student_user.id,
                college_id=c1.id,
                degree="B.Tech",
                branch="Computer Science & Engineering",
                graduation_year=2026,
                cgpa=8.85,
                resume_score=88.5,
                readiness_score=86.0,
                current_stage=StudentStage.SHORTLISTED.value
            )
            db.session.add(demo_student_profile)

            comp_demo = Company(
                name="Acme Tech Innovations",
                industry="Software & AI",
                location="Bengaluru, KA",
                website="https://acme-tech.example.com",
                logo_url="https://placehold.co/200x200/5B21B6/FFFFFF?text=ATI",
                description="Acme Tech Innovations is a leading AI-first software company building next-gen developer tools and ML infrastructure. We're on a mission to democratize AI development for every engineer. Our team comprises ex-Google, Microsoft, and Amazon engineers who believe in building products that developers love."
            )
            db.session.add(comp_demo)
            db.session.flush()

            demo_recruiter_profile = RecruiterProfile(
                user_id=recruiter_user.id,
                company_id=comp_demo.id,
                designation="Lead Campus Recruiter",
                phone="+91 98765 43210"
            )
            db.session.add(demo_recruiter_profile)

            # 3. Skills (30 skills)
            skill_names = [
                ("Python", "Technical"), ("React", "Technical"), ("TypeScript", "Technical"), ("Node.js", "Technical"),
                ("Flask", "Technical"), ("SQL", "Technical"), ("Data Structures", "Technical"), ("Algorithms", "Technical"),
                ("Docker", "Technical"), ("Kubernetes", "Technical"), ("AWS", "Cloud"), ("System Design", "Technical"),
                ("Machine Learning", "AI/ML"), ("PyTorch", "AI/ML"), ("Git", "Tools"), ("CI/CD", "Tools"),
                ("GraphQL", "Technical"), ("MongoDB", "Technical"), ("PostgreSQL", "Technical"), ("Java", "Technical"),
                ("C++", "Technical"), ("Problem Solving", "Core"), ("Agile", "Process"), ("Communication", "Soft"),
                ("Teamwork", "Soft"), ("Leadership", "Soft"), ("Time Management", "Soft"), ("Analytical Thinking", "Soft"),
                ("Cybersecurity", "Security"), ("Linux", "OS")
            ]
            skills_objs = []
            for sname, cat in skill_names:
                s = Skill(name=sname, category=cat)
                db.session.add(s)
                skills_objs.append(s)
            db.session.flush()

            # Add skills to demo student profile
            for sk in skills_objs[:8]:
                db.session.add(StudentSkill(student_id=demo_student_profile.id, skill_id=sk.id, score=random.uniform(75, 95), source='ASSESSMENT'))

            # 4. Companies (10 companies)
            company_data = [
                ("Apex Systems", "Cloud & Enterprise", "https://placehold.co/200x200/06B6D4/FFFFFF?text=AX"),
                ("Nexus Analytics", "Data & AI", "https://placehold.co/200x200/10B981/FFFFFF?text=NX"),
                ("Velocity Financial", "FinTech", "https://placehold.co/200x200/F59E0B/FFFFFF?text=VF"),
                ("CyberGuard Security", "Cybersecurity", "https://placehold.co/200x200/EF4444/FFFFFF?text=CG"),
                ("Quantum Computing Labs", "Deep Tech", "https://placehold.co/200x200/8B5CF6/FFFFFF?text=QC"),
                ("CloudScale Corp", "SaaS", "https://placehold.co/200x200/0EA5E9/FFFFFF?text=CS"),
                ("BioHealth Tech", "HealthTech", "https://placehold.co/200x200/EC4899/FFFFFF?text=BH"),
                ("HyperDrive Motors", "Automotive Tech", "https://placehold.co/200x200/6366F1/FFFFFF?text=HD"),
                ("OmniRetail Global", "E-Commerce", "https://placehold.co/200x200/14B8A6/FFFFFF?text=OR")
            ]
            companies = [comp_demo]
            for name, ind, logo in company_data:
                c = Company(name=name, industry=ind, location="Bengaluru, KA", logo_url=logo)
                db.session.add(c)
                companies.append(c)
            db.session.flush()

            # 5. Job & Internship Postings - Detailed for Acme Tech Innovations (Demo Company)
            acme_jobs = [
                {
                    "title": "Senior Software Engineer - AI Platform",
                    "description": "Build the core AI inference engine that powers our developer tools. You'll work on optimizing model serving, building auto-scaling GPU clusters, and creating delightful developer experiences. This role involves deep systems programming, distributed systems, and ML infrastructure.",
                    "ctc_lpa": 28.0,
                    "min_cgpa": 8.0,
                    "eligible_branches": ["Computer Science & Engineering", "Information Technology", "Electronics & Communication"],
                    "eligible_years": [2025, 2026],
                    "required_skills_json": [
                        {"skill": "Python", "level": 85, "weight": 0.3},
                        {"skill": "System Design", "level": 80, "weight": 0.25},
                        {"skill": "Machine Learning", "level": 75, "weight": 0.2},
                        {"skill": "Docker", "level": 70, "weight": 0.1},
                        {"skill": "Kubernetes", "level": 70, "weight": 0.15}
                    ],
                    "location": "Bengaluru (Hybrid)",
                    "type": "Full-time",
                    "status": "ACTIVE"
                },
                {
                    "title": "Full Stack Engineer - Developer Experience",
                    "description": "Own the end-to-end developer experience for our platform - from SDKs and APIs to documentation and onboarding flows. You'll build tools that thousands of developers use daily. Strong product sense and obsession with DX required.",
                    "ctc_lpa": 22.0,
                    "min_cgpa": 7.5,
                    "eligible_branches": ["Computer Science & Engineering", "Information Technology"],
                    "eligible_years": [2025, 2026],
                    "required_skills_json": [
                        {"skill": "TypeScript", "level": 85, "weight": 0.3},
                        {"skill": "React", "level": 80, "weight": 0.25},
                        {"skill": "Node.js", "level": 75, "weight": 0.2},
                        {"skill": "GraphQL", "level": 70, "weight": 0.15},
                        {"skill": "Python", "level": 65, "weight": 0.1}
                    ],
                    "location": "Bengaluru (Hybrid)",
                    "type": "Full-time",
                    "status": "ACTIVE"
                },
                {
                    "title": "ML Engineer - LLM Fine-tuning",
                    "description": "Fine-tune and optimize LLMs for code generation tasks. Work with our research team to push the boundaries of what AI can do for software development. Publish papers, open-source tools, and ship to production.",
                    "ctc_lpa": 32.0,
                    "min_cgpa": 8.5,
                    "eligible_branches": ["Computer Science & Engineering", "Information Technology", "Electronics & Communication"],
                    "eligible_years": [2025, 2026],
                    "required_skills_json": [
                        {"skill": "Machine Learning", "level": 90, "weight": 0.35},
                        {"skill": "PyTorch", "level": 85, "weight": 0.25},
                        {"skill": "Python", "level": 85, "weight": 0.2},
                        {"skill": "Data Structures", "level": 75, "weight": 0.1},
                        {"skill": "System Design", "level": 70, "weight": 0.1}
                    ],
                    "location": "Bengaluru (On-site)",
                    "type": "Full-time",
                    "status": "ACTIVE"
                },
                {
                    "title": "DevOps Engineer - Cloud Infrastructure",
                    "description": "Design and maintain our multi-cloud infrastructure serving millions of API requests. Build CI/CD pipelines, implement GitOps, and ensure 99.99% uptime. You'll work with AWS, GCP, Kubernetes, and Terraform.",
                    "ctc_lpa": 24.0,
                    "min_cgpa": 7.5,
                    "eligible_branches": ["Computer Science & Engineering", "Information Technology", "Electronics & Communication"],
                    "eligible_years": [2025, 2026],
                    "required_skills_json": [
                        {"skill": "AWS", "level": 85, "weight": 0.3},
                        {"skill": "Kubernetes", "level": 80, "weight": 0.25},
                        {"skill": "Docker", "level": 80, "weight": 0.2},
                        {"skill": "CI/CD", "level": 75, "weight": 0.15},
                        {"skill": "Linux", "level": 70, "weight": 0.1}
                    ],
                    "location": "Bengaluru (Hybrid)",
                    "type": "Full-time",
                    "status": "ACTIVE"
                },
                {
                    "title": "Backend Engineer - Real-time Systems",
                    "description": "Build real-time collaborative features for our IDE plugin - think Figma-style multiplayer editing but for code. WebSockets, CRDTs, operational transforms, and sub-100ms latency.",
                    "ctc_lpa": 26.0,
                    "min_cgpa": 8.0,
                    "eligible_branches": ["Computer Science & Engineering", "Information Technology"],
                    "eligible_years": [2025, 2026],
                    "required_skills_json": [
                        {"skill": "Node.js", "level": 85, "weight": 0.25},
                        {"skill": "System Design", "level": 80, "weight": 0.25},
                        {"skill": "Data Structures", "level": 80, "weight": 0.2},
                        {"skill": "Algorithms", "level": 75, "weight": 0.15},
                        {"skill": "Python", "level": 70, "weight": 0.15}
                    ],
                    "location": "Bengaluru (Hybrid)",
                    "type": "Full-time",
                    "status": "ACTIVE"
                }
            ]

            acme_internships = [
                {
                    "title": "Software Engineering Intern - AI Platform",
                    "description": "Summer 2026 internship (May-July). Work directly with senior engineers on our AI inference platform. You'll contribute to open-source projects, ship features to production, and get mentored by ex-FAANG engineers. High conversion to full-time.",
                    "stipend_pm": 55000.0,
                    "duration_months": 3,
                    "min_cgpa": 7.5,
                    "eligible_branches": ["Computer Science & Engineering", "Information Technology", "Electronics & Communication"],
                    "eligible_years": [2026],
                    "required_skills_json": [
                        {"skill": "Python", "level": 75, "weight": 0.4},
                        {"skill": "Data Structures", "level": 80, "weight": 0.3},
                        {"skill": "Algorithms", "level": 75, "weight": 0.3}
                    ],
                    "location": "Bengaluru (On-site)",
                    "status": "ACTIVE"
                },
                {
                    "title": "Frontend Engineering Intern - Developer Tools",
                    "description": "Build beautiful, performant developer tools. Work on our VS Code extension, CLI, and web dashboard. Learn modern React/TypeScript patterns, testing strategies, and shipping to thousands of developers.",
                    "stipend_pm": 50000.0,
                    "duration_months": 6,
                    "min_cgpa": 7.0,
                    "eligible_branches": ["Computer Science & Engineering", "Information Technology"],
                    "eligible_years": [2026],
                    "required_skills_json": [
                        {"skill": "React", "level": 80, "weight": 0.35},
                        {"skill": "TypeScript", "level": 75, "weight": 0.35},
                        {"skill": "JavaScript", "level": 70, "weight": 0.3}
                    ],
                    "location": "Bengaluru (Hybrid)",
                    "status": "ACTIVE"
                },
                {
                    "title": "ML Research Intern - Code LLMs",
                    "description": "Research internship focused on improving code generation models. Work with our research team on novel architectures, training techniques, and evaluation benchmarks. Potential for paper publications at top ML conferences.",
                    "stipend_pm": 60000.0,
                    "duration_months": 6,
                    "min_cgpa": 8.5,
                    "eligible_branches": ["Computer Science & Engineering", "Information Technology", "Electronics & Communication"],
                    "eligible_years": [2026],
                    "required_skills_json": [
                        {"skill": "Machine Learning", "level": 85, "weight": 0.4},
                        {"skill": "PyTorch", "level": 80, "weight": 0.3},
                        {"skill": "Python", "level": 85, "weight": 0.3}
                    ],
                    "location": "Bengaluru (On-site)",
                    "status": "ACTIVE"
                }
            ]

            job_postings = []
            internship_postings = []

            # Add A cme jobs
            for job_data in acme_jobs:
                jp = JobPosting(company_id=comp_demo.id, **job_data)
                db.session.add(jp)
                job_postings.append(jp)

            # Add Acme internships
            for intern_data in acme_internships:
                ip = InternshipPosting(company_id=comp_demo.id, **intern_data)
                db.session.add(ip)
                internship_postings.append(ip)

            # Add generic jobs for other companies
            for i, c in enumerate(companies[1:], 1):
                jp = JobPosting(
                    company_id=c.id,
                    title=f"Senior SDE - {c.industry}",
                    description=f"Join {c.name} as a full-time software developer working on high-throughput microservices.",
                    ctc_lpa=round(random.uniform(8.0, 24.0), 1),
                    min_cgpa=round(random.uniform(6.5, 8.5), 1),
                    eligible_branches=["Computer Science & Engineering", "Information Technology", "Electronics & Communication"],
                    eligible_years=[2026],
                    required_skills_json=[
                        {"skill": "Python", "level": random.randint(70, 90), "weight": 0.4},
                        {"skill": "React", "level": random.randint(65, 85), "weight": 0.3},
                        {"skill": "SQL", "level": random.randint(60, 80), "weight": 0.3}
                    ]
                )
                ip = InternshipPosting(
                    company_id=c.id,
                    title=f"Software Intern - {c.name}",
                    description=f"6-month immersive software engineering internship at {c.name}.",
                    stipend_pm=float(random.randint(25000, 60000)),
                    min_cgpa=6.5,
                    eligible_branches=["Computer Science & Engineering", "Information Technology"],
                    eligible_years=[2026],
                    required_skills_json=[
                        {"skill": "Python", "level": 70, "weight": 0.5},
                        {"skill": "Data Structures", "level": 75, "weight": 0.5}
                    ]
                )
                db.session.add_all([jp, ip])
                job_postings.append(jp)
                internship_postings.append(ip)

            db.session.flush()

            # Give every posting a realistic deadline so the Opportunities page is populated
            for jp in job_postings:
                if not jp.deadline:
                    jp.deadline = datetime.utcnow() + timedelta(days=random.randint(7, 45))
            for ip in internship_postings:
                if not ip.deadline:
                    ip.deadline = datetime.utcnow() + timedelta(days=random.randint(5, 30))

            db.session.commit()

            # 6. Students (50 students)
            branches = ["Computer Science & Engineering", "Information Technology", "Electronics & Communication", "Mechanical Engineering"]
            stages = [s.value for s in StudentStage]
            students = [demo_student_profile]

            for i in range(1, 50):
                u = User(
                    email=f"student{i}@college.edu",
                    password_hash=pw_hash,
                    name=f"Student Candidate {i}",
                    role=UserRole.STUDENT.value
                )
                db.session.add(u)
                db.session.flush()

                st_stage = random.choice(stages)
                sp = StudentProfile(
                    user_id=u.id,
                    college_id=random.choice([c1.id, c2.id, c3.id]),
                    degree="B.Tech",
                    branch=random.choice(branches),
                    graduation_year=2026,
                    cgpa=round(random.uniform(6.8, 9.8), 2),
                    resume_score=round(random.uniform(60, 98), 1),
                    readiness_score=round(random.uniform(55, 95), 1),
                    current_stage=st_stage
                )
                db.session.add(sp)
                db.session.flush()
                students.append(sp)

                # Add random skills
                for sk in random.sample(skills_objs, 5):
                    db.session.add(StudentSkill(student_id=sp.id, skill_id=sk.id, score=random.uniform(50, 95), source='ASSESSMENT'))

            db.session.flush()

            # 7. Assessments (MCQ + Coding for every skill, plus communication)
            all_assessments = []
            mcq_pools = [
                ("Which statement best describes the role of {s} in a production system?",
                 ["It is optional and can be skipped", "It is a core capability that must be designed carefully", "It only matters at the management level", "It is replaced entirely by cloud providers"],
                 "It is a core capability that must be designed carefully"),
                ("When working with {s}, which approach is considered a best practice?",
                 ["Use ad-hoc fixes and shortcuts", "Follow documented standards and test thoroughly", "Avoid any tooling or automation", "Rely only on memory"],
                 "Follow documented standards and test thoroughly"),
                ("In an interview, how would you demonstrate your {s} skills?",
                 ["Mention it as a keyword only", "Explain past projects with measurable impact", "Say you can learn it quickly", "Copy a solution verbatim"],
                 "Explain past projects with measurable impact"),
                ("Which of these is a common senior-level expectation for {s}?",
                 ["Never documenting decisions", "Mentoring juniors and owning outcomes", "Avoiding code review feedback", "Working in isolation"],
                 "Mentoring juniors and owning outcomes"),
            ]
            coding_pool = "Write a clean, efficient Python function that validates and processes realistic inputs for {s}-based workflows. Include edge-case handling and a short explanation of time complexity."

            for sk in skills_objs:
                ass_mcq = Assessment(skill_id=sk.id, type='mcq', title=f"{sk.name} Technical Proficiency Assessment", duration_min=30, total_marks=100)
                ass_code = Assessment(skill_id=sk.id, type='coding', title=f"{sk.name} Algorithmic Coding Challenge", duration_min=45, total_marks=100, config_json={'language': 'python', 'auto_grade': True})
                db.session.add_all([ass_mcq, ass_code])
                db.session.flush()
                all_assessments.extend([ass_mcq, ass_code])

                for i, (prompt, options, answer) in enumerate(mcq_pools):
                    db.session.add(Question(
                        assessment_id=ass_mcq.id,
                        question_type='mcq',
                        prompt=prompt.format(s=sk.name),
                        options_json=options,
                        correct_answer=answer,
                        difficulty=['easy', 'easy', 'medium', 'hard'][i],
                        marks=25
                    ))
                for i in range(2):
                    db.session.add(Question(
                        assessment_id=ass_code.id,
                        question_type='coding',
                        prompt=coding_pool.format(s=sk.name),
                        difficulty=['medium', 'hard'][i],
                        language='python',
                        test_cases_json=[{"input": "[1, 2, 3]", "expected": "[3, 2, 1]"}],
                        expected_topics_json=[{"skill": sk.name, "weight": 0.8}],
                        marks=50
                    ))

            for sk_name in ["Communication", "Teamwork", "Leadership", "Time Management", "Analytical Thinking"]:
                sk = Skill.query.filter_by(name=sk_name).first()
                if not sk: continue
                ass_comm = Assessment(skill_id=sk.id, type='communication', title=f"{sk_name} Workplace Communication Simulation", duration_min=20, total_marks=50)
                db.session.add(ass_comm)
                db.session.flush()
                for i, (prompt, options, answer) in enumerate(mcq_pools[:3]):
                    db.session.add(Question(
                        assessment_id=ass_comm.id,
                        question_type='mcq',
                        prompt=prompt.format(s=sk_name),
                        options_json=options,
                        correct_answer=answer,
                        difficulty=['easy', 'easy', 'medium'][i],
                        marks=round(50 / 3, 1)
                    ))
                all_assessments.append(ass_comm)
            db.session.flush()

            # 7b. Attempts + Answers so student dashboards show real history
            submitted_statuses = []
            for st in students:
                for i, ass in enumerate(random.sample(all_assessments, min(3, len(all_assessments)))):
                    att = Attempt(
                        student_id=st.id,
                        assessment_id=ass.id,
                        started_at=datetime.utcnow() - timedelta(days=random.randint(3, 30), hours=random.randint(0, 10)),
                        submitted_at=datetime.utcnow() - timedelta(days=random.randint(1, 28), hours=random.randint(0, 8)),
                        score=round(random.uniform(55, 98), 1),
                        status='submitted',
                        proctor_flag=random.random() < 0.1
                    )
                    db.session.add(att)
                    db.session.flush()
                    submitted_statuses.append(att)

                    qs = ass.questions.all()
                    for q in qs[:3]:
                        is_correct = random.random() < 0.75
                        db.session.add(Answer(
                            attempt_id=att.id,
                            question_id=q.id,
                            answer_text="A" if is_correct else random.choice(['B', 'C', 'D']),
                            is_correct=is_correct,
                            awarded_marks=(q.marks if is_correct else 0),
                            language='python' if q.question_type == 'coding' else None,
                            ai_feedback_json={'strength': 'Demonstrates solid grasp of fundamentals.', 'improvement': 'Deepen practice on applied scenarios.'} if is_correct else {'strength': '', 'improvement': 'Revisit core concepts and re-attempt.'}
                        ))

            in_progress_attempt = Attempt(
                student_id=demo_student_profile.id,
                assessment_id=all_assessments[0].id,
                started_at=datetime.utcnow() - timedelta(minutes=12),
                submitted_at=None,
                score=0.0,
                status='in_progress'
            )
            db.session.add(in_progress_attempt)
            db.session.flush()

            # Make sure the demo student has clearly taken a few assessments
            for i, ass in enumerate(all_assessments[1:5]):
                att = Attempt(
                    student_id=demo_student_profile.id,
                    assessment_id=ass.id,
                    started_at=datetime.utcnow() - timedelta(days=10 + i * 2),
                    submitted_at=datetime.utcnow() - timedelta(days=9 + i * 2),
                    score=round(random.uniform(80, 96), 1),
                    status='submitted'
                )
                db.session.add(att)

            # 8. Applications (~300 across all pipeline stages, jobs + internships)
            for st in students:
                for posting in random.sample(job_postings, min(4, len(job_postings))):
                    st_stage = random.choice(stages)
                    app_obj = Application(
                        student_id=st.id,
                        posting_type='JOB',
                        posting_id=posting.id,
                        status=st_stage,
                        match_score=round(random.uniform(65.0, 98.0), 1),
                        missing_skills_json=["Kubernetes", "GraphQL"],
                        eligibility_json={'is_eligible': True}
                    )
                    db.session.add(app_obj)
                    db.session.flush()

                    hist = ApplicationStatusHistory(
                        application_id=app_obj.id,
                        from_status='APPLIED',
                        to_status=st_stage,
                        changed_by='System Seed',
                        reason=f'Initial stage populated as {st_stage}'
                    )
                    db.session.add(hist)

                for posting in random.sample(internship_postings, min(2, len(internship_postings))):
                    st_stage = random.choice(['APPLIED', 'ELIGIBLE', 'SHORTLISTED'])
                    db.session.add(Application(
                        student_id=st.id,
                        posting_type='INTERNSHIP',
                        posting_id=posting.id,
                        status=st_stage,
                        match_score=round(random.uniform(60.0, 97.0), 1),
                        missing_skills_json=["System Design", "Docker"],
                        eligibility_json={'is_eligible': True}
                    ))

            # Give the demo student a rich, realistic history incl. an OFFERED placement
            demo_apps = [
                (job_postings[0], 'OFFERED'),
                (job_postings[2], 'INTERVIEW'),
                (job_postings[3], 'SHORTLISTED'),
                (internship_postings[1], 'SHORTLISTED'),
                (internship_postings[2], 'APPLIED'),
            ]
            for posting, status in demo_apps:
                db.session.add(Application(
                    student_id=demo_student_profile.id,
                    posting_type='JOB' if posting.__class__.__name__ == 'JobPosting' else 'INTERNSHIP',
                    posting_id=posting.id,
                    status=status,
                    match_score=round(random.uniform(82.0, 97.0), 1),
                    missing_skills_json=["GraphQL"],
                    eligibility_json={'is_eligible': True}
                ))

            # 9. Training Programs & Enrollments
            def skill_id(name):
                sk = Skill.query.filter_by(name=name).first()
                return sk.id if sk else None

            training_programs = [
                TrainingProgram(
                    title="Full-Stack Web Development Bootcamp",
                    description="Master React, TypeScript, Flask, and cloud deployment. Build and deploy two industry-grade projects with code reviews from mentors.",
                    instructor="Dr. Priya Sharma",
                    target_skill_id=skill_id("React"),
                    start_date=datetime.utcnow() - timedelta(days=20),
                    end_date=datetime.utcnow() + timedelta(days=40),
                    status="ONGOING"
                ),
                TrainingProgram(
                    title="Data Structures & Algorithms Masterclass",
                    description="LeetCode patterns, problem-solving frameworks, and mock interviews. 120+ curated problems from easy to hard.",
                    instructor="Rajesh Kumar",
                    target_skill_id=skill_id("Algorithms"),
                    start_date=datetime.utcnow() + timedelta(days=7),
                    end_date=datetime.utcnow() + timedelta(days=50),
                    status="UPCOMING"
                ),
                TrainingProgram(
                    title="Machine Learning & Deep Learning Crash Course",
                    description="From linear regression to transformers. Hands-on labs with PyTorch and real datasets.",
                    instructor="Prof. Meera Nair",
                    target_skill_id=skill_id("Machine Learning"),
                    start_date=datetime.utcnow() - timedelta(days=12),
                    end_date=datetime.utcnow() + timedelta(days=25),
                    status="ONGOING"
                ),
                TrainingProgram(
                    title="AWS Cloud & DevOps Essentials",
                    description="EC2, S3, IAM, Docker, Kubernetes, and CI/CD pipelines. Prepare for the AWS Practitioner certification.",
                    instructor="Arun Venkatesh",
                    target_skill_id=skill_id("AWS"),
                    start_date=datetime.utcnow() + timedelta(days=15),
                    end_date=datetime.utcnow() + timedelta(days=55),
                    status="UPCOMING"
                ),
                TrainingProgram(
                    title="System Design Interview Preparation",
                    description="Design scalable systems like Twitter, Uber, and YouTube. Load balancing, caching, SQL vs NoSQL, and CAP theorem.",
                    instructor="Dr. Priya Sharma",
                    target_skill_id=skill_id("System Design"),
                    start_date=datetime.utcnow() - timedelta(days=5),
                    end_date=datetime.utcnow() + timedelta(days=30),
                    status="ONGOING"
                ),
                TrainingProgram(
                    title="Communication & Group Discussion Bootcamp",
                    description="Crack the HR and GD rounds with structured frameworks, mock sessions, and personalized feedback.",
                    instructor="Anita Desai",
                    target_skill_id=skill_id("Communication"),
                    start_date=datetime.utcnow() - timedelta(days=10),
                    end_date=datetime.utcnow() + timedelta(days=10),
                    status="ONGOING"
                ),
                TrainingProgram(
                    title="Python for Data Analysis",
                    description="NumPy, Pandas, and visualization. Bridge theory to practice with weekly projects.",
                    instructor="Karthik R.",
                    target_skill_id=skill_id("Python"),
                    start_date=datetime.utcnow() - timedelta(days=60),
                    end_date=datetime.utcnow() - timedelta(days=7),
                    status="COMPLETED"
                ),
                TrainingProgram(
                    title="Technical Aptitude Acceleration",
                    description="Quantitative aptitude, logical reasoning, and verbal ability focused on campus written tests.",
                    instructor="LearnerLab Faculty",
                    status="COMPLETED"
                ),
            ]
            db.session.add_all(training_programs)
            db.session.flush()

            for prog in training_programs:
                nb = random.randint(3, 12)
                candidate_pool = [s for s in students if s.id != demo_student_profile.id]
                for sp in random.sample(candidate_pool, min(nb, len(candidate_pool))):
                    db.session.add(TrainingEnrollment(
                        program_id=prog.id,
                        student_id=sp.id,
                        status=random.choice(['ENROLLED', 'ENROLLED', 'COMPLETED']),
                        progress_percent=round(random.uniform(20, 100), 1)
                    ))
            db.session.add(TrainingEnrollment(program_id=training_programs[0].id, student_id=demo_student_profile.id, status='ENROLLED', progress_percent=72.0))

            # Placement Drives
            drives = [
                PlacementDrive(
                    title="Campus Placement Drive 2026 - Phase 1",
                    college_id=c1.id,
                    academic_year=2026,
                    start_date=datetime.utcnow() - timedelta(days=10),
                    end_date=datetime.utcnow() + timedelta(days=30),
                    status="ACTIVE",
                    description="Main campus placement drive for the Class of 2026. 40+ companies, 300+ roles across IT, core, and analytics."
                ),
                PlacementDrive(
                    title="Dream Company Mega Drive",
                    college_id=c1.id,
                    academic_year=2026,
                    start_date=datetime.utcnow() + timedelta(days=21),
                    end_date=datetime.utcnow() + timedelta(days=60),
                    status="UPCOMING",
                    description="Top product companies with 20+ LPA packages. Includes pre-placement talks and mock tests."
                ),
                PlacementDrive(
                    title="IT & Software Services Drive",
                    college_id=c2.id,
                    academic_year=2026,
                    start_date=datetime.utcnow() - timedelta(days=5),
                    end_date=datetime.utcnow() + timedelta(days=20),
                    status="ACTIVE",
                    description="Service-based companies hiring for software, testing, and support roles with 3-8 LPA packages."
                ),
                PlacementDrive(
                    title="Data Science & Analytics Recruitment",
                    college_id=c2.id,
                    academic_year=2026,
                    start_date=datetime.utcnow() + timedelta(days=40),
                    end_date=datetime.utcnow() + timedelta(days=75),
                    status="UPCOMING",
                    description="Analytics and AI-first companies recruiting for data analyst, scientist, and BI engineer roles."
                ),
                PlacementDrive(
                    title="Class of 2025 Placement Drive",
                    college_id=c1.id,
                    academic_year=2025,
                    start_date=datetime.utcnow() - timedelta(days=120),
                    end_date=datetime.utcnow() - timedelta(days=10),
                    status="COMPLETED",
                    description="Final placement drive for the Class of 2025. 900+ offers rolled out across all branches."
                ),
                PlacementDrive(
                    title="Core & GovTech Drive 2026",
                    college_id=c3.id,
                    academic_year=2026,
                    start_date=datetime.utcnow() + timedelta(days=60),
                    end_date=datetime.utcnow() + timedelta(days=90),
                    status="UPCOMING",
                    description="Core engineering and government-tech companies including PSUs and defense research organizations."
                ),
            ]
            db.session.add_all(drives)

            # 10. Notifications
            n1 = Notification(user_id=student_user.id, title="Application Shortlisted", message="Congratulations! You have been shortlisted for Senior SDE at Acme Tech Innovations.", type="success", is_read=False)
            n2 = Notification(user_id=student_user.id, title="Upcoming Assessment", message="Your Python Technical Proficiency Assessment is scheduled for tomorrow.", type="info", is_read=False)
            n3 = Notification(user_id=admin_user.id, title="New Drive Created", message="Campus Placement Drive 2026 has been published to all eligible students.", type="info", is_read=True)
            n4 = Notification(user_id=recruiter_user.id, title="New Applications Received", message="25 new candidates have applied for Senior SDE - Software & AI.", type="info", is_read=False)
            n5 = Notification(user_id=student_user.id, title="Interview Scheduled", message="Technical Round 1 is scheduled for Senior Software Engineer - AI Platform on the coming Friday at 11:00 AM (online).", type="info", is_read=False)
            n6 = Notification(user_id=student_user.id, title="Offer Letter Ready", message="Congratulations! Your offer letter for the ML Engineer role has been generated. Review it from your dashboard.", type="success", is_read=False)
            n7 = Notification(user_id=student_user.id, title="New Job Matches Your Skills", message="DevOps Engineer - Cloud Infrastructure at Acme Tech Innovations is a 92% match for your profile.", type="info", is_read=False)
            n8 = Notification(user_id=student_user.id, title="Placement Drive Update", message="Dream Company Mega Drive is now open. 20+ LPA packages. Register before the deadline.", type="info", is_read=False)
            n9 = Notification(user_id=student_user.id, title="Training Enrollment", message="You are enrolled in the Full-Stack Web Development Bootcamp. Session 4 starts tomorrow.", type="info", is_read=True)
            n10 = Notification(user_id=student_user.id, title="Resume Score Improved", message="Your resume ATS score improved to 88! Your profile is now in the top 5% of the batch.", type="success", is_read=True)
            n11 = Notification(user_id=student_user.id, title="Application Deadline Reminder", message="The Frontend Engineering Intern deadline closes in 3 days. Apply soon if you haven't yet.", type="warning", is_read=False)
            db.session.add_all([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11])

            # 11. Sample Interviews for Industry Portal
            # Get some applications for the demo company's jobs
            acme_job_ids = [jp.id for jp in job_postings if jp.company_id == comp_demo.id]
            applications_for_interviews = Application.query.filter(Application.posting_id.in_(acme_job_ids)).limit(10).all()


            interview_data = [
                {
                    "application_id": applications_for_interviews[0].id if len(applications_for_interviews) > 0 else None,
                    "title": "Technical Round 1 - System Design & Coding",
                    "scheduled_at": datetime.utcnow() + timedelta(days=2, hours=10),
                    "duration_min": 60,
                    "mode": "ONLINE",
                    "meeting_link": "https://meet.google.com/acm-tch-nov",
                    "interviewer_name": "Dr. Priya Sharma",
                    "location": "Bengaluru Office / Online",
                    "feedback_notes": "Focus on distributed systems design and Python coding. Candidate has strong ML background."
                },
                {
                    "application_id": applications_for_interviews[1].id if len(applications_for_interviews) > 1 else None,
                    "title": "Technical Round 2 - Deep Dive on Projects",
                    "scheduled_at": datetime.utcnow() + timedelta(days=3, hours=14),
                    "duration_min": 45,
                    "mode": "ONLINE",
                    "meeting_link": "https://meet.google.com/acm-tch-dec",
                    "interviewer_name": "Rajesh Kumar",
                    "location": "Bengaluru Office / Online",
                    "feedback_notes": "Deep dive into resume projects. Ask about scale, trade-offs, and learnings."
                },
                {
                    "application_id": applications_for_interviews[2].id if len(applications_for_interviews) > 2 else None,
                    "title": "Behavioral & Culture Fit Round",
                    "scheduled_at": datetime.utcnow() + timedelta(days=4, hours=11),
                    "duration_min": 45,
                    "mode": "ONLINE",
                    "meeting_link": "https://meet.google.com/acm-tch-jan",
                    "interviewer_name": "Sarah Jenkins",
                    "location": "Bengaluru Office / Online",
                    "feedback_notes": "Culture fit, career goals, and team collaboration style. Standard behavioral questions."
                },
                {
                    "application_id": applications_for_interviews[3].id if len(applications_for_interviews) > 3 else None,
                    "title": "Final Round - VP Engineering",
                    "scheduled_at": datetime.utcnow() + timedelta(days=5, hours=16),
                    "duration_min": 30,
                    "mode": "ONLINE",
                    "meeting_link": "https://meet.google.com/acm-tch-feb",
                    "interviewer_name": "Arun Venkatesh",
                    "location": "Bengaluru Office / Online",
                    "feedback_notes": "Final sell round. Discuss vision, growth path, and offer details."
                },
                {
                    "application_id": applications_for_interviews[4].id if len(applications_for_interviews) > 4 else None,
                    "title": "Coding Assessment - Live Pair Programming",
                    "scheduled_at": datetime.utcnow() + timedelta(days=1, hours=9),
                    "duration_min": 90,
                    "mode": "ONLINE",
                    "meeting_link": "https://codeshare.io/acme-interview-001",
                    "interviewer_name": "Karthik R.",
                    "location": "Bengaluru Office / Online",
                    "feedback_notes": "Live coding session. Build a small feature end-to-end. Evaluate code quality, testing, and communication."
                }
            ]

            for int_data in interview_data:
                if int_data["application_id"]:
                    interview = Interview(**int_data)
                    db.session.add(interview)
                    
                    # Update application status
                    app_obj = db.session.get(Application, int_data["application_id"])
                    if app_obj and app_obj.status not in ['INTERVIEW_SCHEDULED', 'OFFERED', 'PLACED']:
                        app_obj.status = 'INTERVIEW_SCHEDULED'

            # 12. Additional Recruiter Notifications
            rn1 = Notification(user_id=recruiter_user.id, title="Interview Scheduled", message="Technical Round 1 scheduled for 5 candidates this week.", type="info", is_read=False)
            rn2 = Notification(user_id=recruiter_user.id, title="New Job Posting Live", message="Senior Software Engineer - AI Platform is now live and receiving applications.", type="success", is_read=False)
            rn3 = Notification(user_id=recruiter_user.id, title="Candidate Pool Update", message="15 new candidates match your Senior SDE - AI Platform requirements (80%+ match).", type="info", is_read=True)
            db.session.add_all([rn1, rn2, rn3])

            db.session.commit()

            print("✅ Seeding complete!")
            print("──────────────────────────────────────────────────")
            print("DEMO ACCOUNTS READY:")
            print("  Student:   student@demo.com   / Demo@1234")
            print("  Admin:     admin@demo.com     / Demo@1234")
            print("  Recruiter: recruiter@demo.com / Demo@1234")
            print("──────────────────────────────────────────────────")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Seeding Failed: {e}")
            raise e

if __name__ == '__main__':
    seed_db()
