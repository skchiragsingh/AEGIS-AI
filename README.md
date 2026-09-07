**AEGIS-AI**

**Autonomous AI Incident Response & SRE Platform**

AEGIS-AI is an AI-powered incident response and AIOps platform designed to detect system incidents, investigate their root causes, retrieve relevant operational knowledge, generate recovery plans, and safely execute approved recovery actions.

The project combines monitoring, AI-driven investigation, RAG, recovery planning, safety guardrails, and human approval into a single incident-response workflow.

---

 **Architecture**


                    Monitoring
                        |
                        v
                Incident Detection
                        |
                        v
               Incident Processing
                        |
                        v
                    AI Triage
                        |
                        v
                AI Investigation
                        |
                 +------+------+
                 |             |
                 v             v
                RAG           LLM
                 |             |
                 +------+------+
                        |
                        v
              Recovery Planning
                        |
                        v
                   Guardrails
                        |
              +---------+---------+
              |                   |
              v                   v
       Auto Execution       Human Approval
              |                   |
              +---------+---------+
                        |
                        v
              Recovery Executor
                        |
                        v
                Incident History
