#!/usr/bin/env python3
"""
Extract proper concepts from bootcamp PDF topics.
This creates meaningful learning concepts based on the actual curriculum.
"""
import asyncio
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.db import Concept, ConceptEdge, ContentChunk
from app.services.ollama_router import OllamaRouter
from app.services.quiz_service import QuizService
from app.services.learning_service import LearningService

# Real bootcamp topics from BB101 PDF
BOOTCAMP_TOPICS = [
    {
        "name": "IBM Sterling B2B Integrator Architecture",
        "why_it_matters": "Understanding the architecture is fundamental to implementing and troubleshooting B2Bi solutions. It's the foundation for all other concepts.",
        "intuition": "Think of B2Bi as a central hub that connects different trading partners, protocols, and systems. The architecture defines how data flows through this hub.",
        "explanation": "B2Bi provides a platform for secure B2B data exchange with components like Administration Console, Map Editor, GPM, and Mailbox Interface working together.",
        "example": "In a real implementation, purchase orders flow from trading partners through SFTP into mailboxes, get processed by business processes, and routed to backend systems.",
        "common_mistake": "Treating B2Bi as just a file transfer tool instead of understanding it as a complete integration platform with workflow, transformation, and routing capabilities.",
        "checkpoint_question": "What are the four main user interfaces in B2Bi and what is each one used for?",
        "hard_follow_up": "How would you design a B2Bi architecture to handle 10,000 transactions per hour with high availability requirements?",
        "source_reference": "BB101-IBM_STERLING_B2Bi_AND_SFG-Bootcamp-Topics-v1.0.pdf - Day 1, Lesson 4"
    },
    {
        "name": "Mailbox Concept in Sterling Integrator",
        "why_it_matters": "Mailboxes are the primary mechanism for organizing and securing file transfers between trading partners. Every B2Bi implementation uses mailboxes.",
        "intuition": "Think of mailboxes like email inboxes - each trading partner has their own secure space to send and receive files, with permissions controlling who can access what.",
        "explanation": "Mailboxes provide isolated storage areas for trading partners with configurable permissions, virtual roots for security, and integration with business processes for automated file handling.",
        "example": "Create a mailbox for partner 'ACME Corp' with path /mailbox/acme, set read/write permissions, and configure a business process to automatically pick up files when they arrive.",
        "common_mistake": "Not properly configuring virtual roots, leading to security vulnerabilities where partners can access each other's files.",
        "checkpoint_question": "What is a virtual root and why is it important for mailbox security?",
        "hard_follow_up": "Design a mailbox structure for 50 trading partners with different security requirements and explain your permission strategy.",
        "source_reference": "BB101-IBM_STERLING_B2Bi_AND_SFG-Bootcamp-Topics-v1.0.pdf - Day 2, Lesson 5"
    },
    {
        "name": "SFTP Protocol in B2Bi",
        "why_it_matters": "SFTP is the most common secure file transfer protocol in enterprise B2B. Understanding SFTP is essential for 90% of B2Bi implementations.",
        "intuition": "SFTP is like a secure tunnel for files - it uses SSH encryption to protect data in transit, unlike regular FTP which sends everything in plain text.",
        "explanation": "SFTP (SSH File Transfer Protocol) provides encrypted file transfer using SSH keys or passwords for authentication. B2Bi acts as an SFTP server, allowing trading partners to connect and transfer files securely.",
        "example": "Trading partner connects to B2Bi using SFTP client (like WinSCP) with SSH key authentication, uploads an EDI 850 purchase order to their mailbox, triggering automated processing.",
        "common_mistake": "Confusing SFTP with FTPS - they are completely different protocols. SFTP uses SSH (port 22), FTPS uses SSL/TLS (ports 989/990).",
        "checkpoint_question": "How does SFTP authentication work in B2Bi and what are the two main authentication methods?",
        "hard_follow_up": "A trading partner reports SFTP connection failures. Walk through your troubleshooting steps including SSH key validation, firewall rules, and B2Bi logs.",
        "source_reference": "BB101-IBM_STERLING_B2Bi_AND_SFG-Bootcamp-Topics-v1.0.pdf - Day 2, Lesson 6"
    },
    {
        "name": "Business Process Development with GPM",
        "why_it_matters": "Business Processes are the automation engine of B2Bi. They define how files are processed, transformed, and routed - the core of any B2Bi solution.",
        "intuition": "Think of a Business Process like a flowchart that executes automatically. Each box is a service (read file, transform, route) connected by arrows showing the flow.",
        "explanation": "The Graphical Process Modeler (GPM) provides a visual interface to create workflows using drag-and-drop services. Business Processes can be triggered manually, by schedule, or by events like file arrival.",
        "example": "Create a BP that: 1) Extracts file from mailbox, 2) Validates XML structure, 3) Transforms using map, 4) Routes to backend system via HTTP, 5) Sends acknowledgment back to partner.",
        "common_mistake": "Not implementing proper error handling - BPs should have exception paths to handle failures gracefully and send alerts.",
        "checkpoint_question": "What is the difference between checking in and checking out a Business Process, and why does version control matter?",
        "hard_follow_up": "Design a Business Process that handles EDI 850 orders with validation, duplicate detection, transformation, routing, and error notification. Explain each service choice.",
        "source_reference": "BB101-IBM_STERLING_B2Bi_AND_SFG-Bootcamp-Topics-v1.0.pdf - Day 3, Lesson 7-8"
    },
    {
        "name": "XPath for Data Extraction",
        "why_it_matters": "XPath is essential for extracting data from XML documents in B2Bi. Most EDI and business documents are XML-based, making XPath a critical skill.",
        "intuition": "XPath is like a GPS for XML - it provides a path to navigate to specific data elements within an XML document structure.",
        "explanation": "XPath uses path expressions to select nodes in XML documents. In B2Bi, XPath is used in business processes to extract values, make routing decisions, and populate variables.",
        "example": "Use XPath '/PurchaseOrder/OrderHeader/OrderNumber' to extract order number from XML, then use it in filename or routing logic.",
        "common_mistake": "Not understanding the difference between absolute paths (/root/element) and relative paths (//element) - this causes unexpected results.",
        "checkpoint_question": "Write an XPath expression to extract all line items from a purchase order where quantity is greater than 100.",
        "hard_follow_up": "Given a complex nested XML structure with namespaces, write XPath to extract specific values and explain how namespace prefixes affect the expression.",
        "source_reference": "BB101-IBM_STERLING_B2Bi_AND_SFG-Bootcamp-Topics-v1.0.pdf - Day 3, Lesson 9"
    },
    {
        "name": "Routing Rules and Channels",
        "why_it_matters": "Routing Rules automate the triggering of Business Processes based on file arrival or other events. They're the glue between mailboxes and processing logic.",
        "intuition": "Routing Rules are like mail sorting rules - 'when a file arrives in this mailbox with this pattern, automatically run this Business Process'.",
        "explanation": "Routing Rules define conditions (file pattern, mailbox path, document type) and actions (execute BP, move file). They enable event-driven automation in B2Bi.",
        "example": "Create routing rule: When file matching '*.xml' arrives in /mailbox/acme/inbound, execute BP 'ProcessACMEOrder' with the file as input.",
        "common_mistake": "Creating overlapping routing rules that cause the same file to be processed multiple times, or rules that are too broad and match unintended files.",
        "checkpoint_question": "What are the key components of a Routing Rule and how do you prevent duplicate processing?",
        "hard_follow_up": "Design a routing strategy for 20 trading partners where some send multiple document types to the same mailbox. How do you ensure correct processing?",
        "source_reference": "BB101-IBM_STERLING_B2Bi_AND_SFG-Bootcamp-Topics-v1.0.pdf - Day 3, Lab Exercise"
    },
    {
        "name": "Partner User Management",
        "why_it_matters": "Proper partner user configuration is critical for security and access control. Each trading partner needs appropriate permissions and authentication.",
        "intuition": "Partner users are like employee accounts - each has specific permissions, authentication credentials, and access to only their designated areas.",
        "explanation": "Partner users in B2Bi have profiles defining authentication methods (password, SSH key, certificate), mailbox access, and permissions. They're separate from internal admin users.",
        "example": "Create partner user 'acme_user' with SSH key authentication, grant read/write access to /mailbox/acme, restrict access to other mailboxes.",
        "common_mistake": "Using the same credentials for multiple partners or giving partners admin-level access instead of restricting to their specific mailboxes.",
        "checkpoint_question": "What's the difference between a partner user and an admin user in B2Bi, and what permissions should each have?",
        "hard_follow_up": "A partner reports they can see another partner's files. Diagnose the security misconfiguration and explain how to prevent it.",
        "source_reference": "BB101-IBM_STERLING_B2Bi_AND_SFG-Bootcamp-Topics-v1.0.pdf - Day 2, Lesson 5"
    },
    {
        "name": "Map Editor and Data Transformation",
        "why_it_matters": "Data transformation is required in almost every B2B integration - converting between EDI, XML, JSON, and custom formats. Map Editor is the primary tool.",
        "intuition": "Map Editor is like a translator - it takes data in one format (source) and converts it to another format (target) using visual mapping rules.",
        "explanation": "Sterling Map Editor provides graphical interface to map fields between source and target schemas. It supports EDI standards, XML, flat files, and custom formats with built-in functions for data manipulation.",
        "example": "Map EDI 850 purchase order to internal XML format: map BEG02 to OrderNumber, map N1 loop to ShipTo address, apply date format conversion.",
        "common_mistake": "Not handling optional fields or repeating segments correctly, causing map failures when data structure varies.",
        "checkpoint_question": "What are the main components of a map in Sterling Map Editor and how do you test a map before deploying?",
        "hard_follow_up": "Design a map to convert EDI 850 to JSON API format, handling multiple line items, optional fields, and data type conversions. Explain your approach.",
        "source_reference": "BB101-IBM_STERLING_B2Bi_AND_SFG-Bootcamp-Topics-v1.0.pdf - Mapping folder"
    }
]

async def main():
    print("Extracting proper bootcamp concepts...")
    print(f"Will create {len(BOOTCAMP_TOPICS)} concepts from curriculum\n")
    
    with SessionLocal() as db:
        router = OllamaRouter()
        quiz = QuizService(db, router)
        learning = LearningService(db)
        
        try:
            # Delete existing bad concepts (keep demo-sftp)
            print("Cleaning up incorrect concepts...")
            bad_concepts = db.scalars(
                select(Concept).where(Concept.id != "demo-sftp")
            ).all()
            for concept in bad_concepts:
                print(f"  Removing: {concept.name}")
                db.delete(concept)
            db.commit()
            
            # Create proper concepts
            print("\nCreating proper bootcamp concepts...")
            created_concepts = []
            for topic in BOOTCAMP_TOPICS:
                concept = Concept(
                    name=topic["name"],
                    why_it_matters=topic["why_it_matters"],
                    intuition=topic["intuition"],
                    explanation=topic["explanation"],
                    example=topic["example"],
                    common_mistake=topic["common_mistake"],
                    checkpoint_question=topic["checkpoint_question"],
                    hard_follow_up=topic["hard_follow_up"],
                    source_reference=topic["source_reference"],
                )
                db.add(concept)
                db.flush()
                created_concepts.append(concept)
                print(f"  ✓ Created: {concept.name}")
            
            db.commit()
            
            # Build prerequisite edges (sequential learning path)
            print("\nBuilding prerequisite edges...")
            edge_count = 0
            for i in range(len(created_concepts) - 1):
                edge = ConceptEdge(
                    source_concept_id=created_concepts[i].id,
                    target_concept_id=created_concepts[i + 1].id,
                    edge_type="prerequisite_for"
                )
                db.add(edge)
                edge_count += 1
                print(f"  {created_concepts[i].name} → {created_concepts[i + 1].name}")
            
            db.commit()
            
            # Generate quiz questions
            print("\nGenerating quiz questions...")
            quiz_count = await quiz.ensure_questions()
            print(f"✅ Generated {quiz_count} quiz questions")
            
            # Ensure learner profiles
            print("\nEnsuring learner profiles...")
            learning.ensure_profiles(user_id="demo-user")
            print("✅ Learner profiles ready")
            
            print("\n🎉 Proper concept extraction complete!")
            print(f"   - {len(created_concepts)} meaningful concepts")
            print(f"   - {edge_count} prerequisite edges")
            print(f"   - {quiz_count} quiz questions")
            print("\nConcepts follow the actual BB101 bootcamp curriculum!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
