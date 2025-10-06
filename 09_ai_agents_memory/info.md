# 🧠 Memory in AI Agents

## 📘 What is Memory?

In **AI agents**, **memory** refers to the ability of an agent to **remember information from past interactions** and **use it later** to make smarter decisions or provide better responses.

Just like humans, an agent with memory doesn’t start fresh every time — it learns and adapts based on what it remembers.

---

## 💡 Simple Definition

> **Memory in AI agents** is a way to store and recall previous data, messages, or states, so the agent can act more intelligently over time.

---

## 💬 Example 1 — Chatbot Agent

Imagine a customer support AI agent:

**Without Memory:**
User: Hi, my internet is not working.
AI: What’s your connection ID?
User: It’s 12345.
User: It started working now.
AI: What’s your connection ID again?

**With Memory:**
User: Hi, my internet is not working.
AI: What’s your connection ID?
User: It’s 12345.
User: It started working now.
AI: Glad it’s working again! I’ve updated your account (ID 12345).

✅ The agent **remembers** your connection ID from the past and uses it later.

---

## ⚙️ Example 2 — LangChain or LangGraph Agent

In frameworks like **LangChain**, memory can store:

- **Chat history** — previous messages between user and agent.
- **User preferences** — name, interests, or context.
- **Intermediate results** — data fetched from APIs or databases.

Example:

> User: "Summarize our last chat."  
> Agent: _(recalls stored conversation and summarizes it)_

---

## 🧩 Types of Memory

| Type                 | Description                                               | Example                                |
| -------------------- | --------------------------------------------------------- | -------------------------------------- |
| 🕐 Short-Term Memory | Remembers recent conversation (context window)            | Keeps last few user messages           |
| 📚 Long-Term Memory  | Stores information permanently (database or vector store) | User preferences, facts                |
| ⚙️ Working Memory    | Holds temporary reasoning steps                           | Calculations or chain-of-thought steps |

---

## 🧠 Why Memory Matters

- Makes conversations **more natural**
- Helps agents **learn and personalize**
- Enables **context-aware** reasoning
- Reduces **repetition** and improves user experience

---

## 🚀 Want to Implement Memory?

In LangChain, you can easily add memory to an agent like this:

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

memory = ConversationBufferMemory()
llm = ChatOpenAI(model="gpt-4o-mini")

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

conversation.predict(input="Hi, my name is Rishikesh.")
conversation.predict(input="What is my name?")
```

**Output**
Your name is Rishikesh.
