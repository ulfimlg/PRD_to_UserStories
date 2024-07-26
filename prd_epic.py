from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import autogen

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json",
)
# Create the agents
user_proxy = UserProxyAgent(
    name="Human",
    system_message="A human user who initiates the task and receives the final output.",
    code_execution_config=False,
    human_input_mode="NEVER",  # Add this line to prevent asking for human input
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: "FINAL EPICS:" in x.get("content", "")
)

product_manager = AssistantAgent(
    name="Product_Manager",
    system_message="""You are an experienced Product Manager leading the process of converting PRDs into epics.

        Your role:
        1. Break down the Product Requirement Document into a list of multiple epics.
        2. Actively engage other agents in discussion about epic definition and refinement.
        3. Ask for specific input from each agent based on their expertise.
        4. Synthesize feedback to refine epic definitions.
        5. Create a final set of epics after asking inputs from all the agents(Product Owner, Technical Lead, Dev Team Rep)
        6. Make final decisions on epic definitions and priorities after thorough discussion.


        Critical instructions:
        - You MUST interact with other agents. Do not simulate or imagine their responses.
        - Ask direct questions to specific agents and wait for their actual responses.
        - Do not proceed to the next step until you have received actual input from other agents.
        - Ensure thorough collaboration before finalizing epics.
        - Your final message must be directed to the Human (UserProxy) agent and contain ONLY:
        1. The numbered list of FINAL EPICS with detailed descriptions
        2. The statement "PROCESS COMPLETE. TERMINATING GROUPCHAT."
        - Do not suggest any next steps or further actions.
        - After sending the final epics to the Human (UserProxy) agent, do not respond to any further messages.""",
        llm_config={
            "config_list":config_list
        }
        )

product_owner = AssistantAgent(
    name="Product_Owner",
    system_message="""You are a seasoned Product Owner supporting the Product Manager in defining epics.

        When asked for input:
        1. Answer the Product Manager's question directly and concisely.
        2. Provide insights on potential user stories within proposed epics.
        3. Offer perspective on epic alignment with sprint planning.
        4. Collaborate on epic sizing feasibility.
        5. Suggest improvements or additions to proposed epics based on user needs.
        6. Always end your message with "Next speaker: Product Manager".


        Critical instructions:
        - Only respond when directly addressed by the Product Manager or other agents.
        - Provide specific insights based on your expertise as a Product Owner.
        - Do not draft complete epics yourself; focus on providing input to refine the Product Manager's proposals.
        - Do not answer on behalf of other agents or simulate their responses.""",
            llm_config={
                "config_list":config_list
            }
        )

technical_lead = AssistantAgent(
    name="Technical_Lead",
    system_message="""You are a Technical Lead providing technical insights on proposed epics.

        When asked for input:
        1. Answer the Product Manager's question directly and concisely.
        2. Evaluate technical feasibility of proposed epics.
        3. Identify technical dependencies between epics.
        4. Suggest architectural approaches and highlight constraints.
        5. Collaborate on technical complexity assessments.
        6. Always end your message with "Next speaker: Product Manager".

        Critical instructions:
        - Work only with other AI agents. Do not involve the Human user.
        - Do not suggest next steps or further actions after FINAL EPICS are listed.
        - Your role ends when the Product Manager lists the FINAL EPICS.
        - Do not respond to any messages after the Product Manager has terminated the chat.""",
            llm_config={
                "config_list":config_list
            }
        )

dev_team_rep = AssistantAgent(
    name="Dev_Team_Rep",
    system_message="""You are a Senior Developer providing implementation insights for epic definition.

        When asked for input:
        1. Answer the Product Manager's question directly and concisely.
        1. Provide input on development effort for proposed epics.
        2. Identify potential implementation challenges or risks.
        3. Suggest approaches to break down epics into manageable tasks.
        4. Offer insights on testing and quality assurance considerations.
        5. Always end your message with "Next speaker: Product Manager".

        Critical instructions:
        - Only respond when directly addressed by the Product Manager or other agents.
        - Provide specific development insights based on your expertise.
        - Do not draft complete epics yourself; focus on providing implementation input to refine the Product Manager's proposals.
        - Do not answer on behalf of other agents or simulate their responses.""",
            llm_config={
                "config_list":config_list
            }
        )
# Create the GroupChat
groupchat = GroupChat(
    agents=[user_proxy,product_manager, product_owner, technical_lead, dev_team_rep],
    messages=[],
    max_round=50
)

# Create the GroupChatManager
manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

# Function to initiate the conversation
def start_prd_to_epic_conversion(prd):
    chat_result  = user_proxy.initiate_chat(
        manager,
        message=f"Here's the PRD for our new project. Please convert this into a set of epics: {prd}",
        
    )

    return chat_result

