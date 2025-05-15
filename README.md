# 🔍 **PolygraphGPT**: A Multimodal AI System for Attribution and Deception Detection in Cyber Influence and Hybrid Warfare

*Perplexity Hackathon 2025 Submission*  
*Powered by Perplexity Sonar API*  

---

## 💡 **Project Overview**

**PolygraphGPT** is an AI-driven system designed to combat the increasing threat of hybrid warfare, misinformation, and cyber-influence operations. With the rise of AI-driven misinformation campaigns, deepfakes, and malicious content, organizations and governments are struggling to detect and attribute deceptive narratives. **PolygraphGPT** addresses this issue by leveraging advanced **Natural Language Processing (NLP)**, **machine learning**, and **AI-driven research tools** to provide a cutting-edge solution for attribution and deception detection.

**PolygraphGPT** is capable of analyzing, identifying, and attributing deceptive content across multiple platforms, including social media, emails, and online forums. By combining **linguistic forensics**, **behavioral anomaly detection**, and **cognitive fingerprinting**, the system provides unparalleled insights into the motives behind cyber-influence campaigns, phishing operations, and deepfake attacks.

---

## 🌐 **Inspiration & Use Case**

The growing sophistication of cyber-influence operations, particularly from state-sponsored actors, has made it increasingly difficult to differentiate between genuine communication and manipulated content. These operations often combine multiple deceptive tactics, such as:

- **Phishing attacks** (using social engineering and malicious links).
- **Misinformation campaigns** (targeting specific ideologies or countries).
- **Deepfake content** (audio, video, or images designed to deceive).

**PolygraphGPT** aims to fill this critical gap by using AI to identify **linguistic manipulation** and detect **AI-generated deception** in a scalable and cross-lingual manner. This system not only helps detect deceptive content but also assists in attributing the source of the operation, potentially revealing the threat actors behind these campaigns.

---

## 🔥 **Key Features**

- **🧠 Multimodal Deception Detection**  
  PolygraphGPT integrates multiple AI models to detect deception across different media (text, audio, video). It uses **NLP models** to identify manipulative language patterns and **deepfake detection** models to analyze media for authenticity.

- **🔎 Attribution Through Linguistic Forensics**  
  The system employs **linguistic fingerprinting** to analyze text and identify recurring styles of known threat actors (e.g., Russian GRU or Iranian APT groups). It also maps the **geopolitical context** of the language to trace back the possible source.

- **💡 Cognitive Fingerprinting**  
  By analyzing the cognitive styles and psychological manipulation tactics embedded in phishing emails and misinformation campaigns, PolygraphGPT can identify subtle cues that hint at manipulation, such as persuasive language techniques or narrative arcs typical of certain groups.

- **🧪 Cross-Lingual and Multiplatform Support**  
  With **multilingual support** (Arabic, Russian, Mandarin), PolygraphGPT can detect manipulation in a variety of languages, making it suitable for global-scale influence operations. It integrates **Perplexity Sonar** for internet-scale research, collecting data across various platforms like social media, news articles, and hacker forums.

- **🔄 Real-Time Attribution**  
  The system can query **live sources** and track **ongoing campaigns** to provide real-time attribution, using a **knowledge graph** to track adversarial tactics and techniques (TTPs) across different influence campaigns.

---

## 🔧 **Tech Stack**

The core of PolygraphGPT is built using **Python** for its flexibility in handling AI models and large datasets, alongside **SQL** for data storage and management. Here’s the breakdown of the tech stack:

| Component                 | Technology Used                                       |
|---------------------------|-------------------------------------------------------|
| **Backend**               | Python (Flask or Django for API services)             |
| **AI Integration**        | Pre-trained NLP models (transformers, GPT-4)         |
| **Deep Learning**         | PyTorch or TensorFlow (for deepfake detection models) |
| **Deception Detection**   | NLTK, spaCy, TextBlob (for linguistic analysis)       |
| **Research & Querying**   | Perplexity Sonar API (real-time threat research)      |
| **Database**              | SQL (MySQL/PostgreSQL for storing threat data)        |
| **Data Processing**       | Pandas, NumPy, and Scikit-learn (for data analysis)   |
| **Multilingual Support**  | Google Translate API, multilingual NLP models        |

---

## 🔍 Perplexity Sonar Integration

SentientSOC integrates with the **Perplexity Sonar API** to provide the **Threat Hunter** agent with real-time threat intelligence data. This allows the system to detect active cyber threats by accessing up-to-date information on malware, attacker infrastructure, phishing campaigns, and Indicators of Compromise (IoCs).

Using Perplexity Sonar enhances SentientSOC’s ability to:

- Continuously monitor emerging threats beyond static or simulated data.
- Correlate live threat intelligence with historical incident memory stored in the SQL database.
- Enable collaborative, context-aware decision-making across autonomous agents.

This real-time intelligence feed is a key component in demonstrating SentientSOC’s capacity to operate as a next-generation autonomous Security Operations Center.

---

## 🚀 **How It Works**

PolygraphGPT follows a multi-step process to detect deception, analyze narratives, and attribute influence campaigns. Here’s a step-by-step breakdown of how the system works:

### 1️⃣ **Input Data Collection**

Users submit suspicious content (e.g., emails, social media posts, or videos). The system can also continuously monitor platforms for potential influence campaigns.

### 2️⃣ **Linguistic Forensics & Analysis**

- **Text Processing**: PolygraphGPT uses NLP techniques (e.g., tokenization, part-of-speech tagging, and sentiment analysis) to examine the language used in the content.
- **Deceptive Patterns**: The system identifies manipulative language patterns, cognitive bias triggers, and hallucinatory narratives typical of phishing or misinformation campaigns.

### 3️⃣ **Deepfake Detection (For Multimedia)**

- For multimedia inputs (audio/video), PolygraphGPT uses deep learning models trained to recognize deepfake manipulations, leveraging **computer vision** and **audio analysis** to authenticate the content.

### 4️⃣ **Cognitive Fingerprinting**

The system analyzes the psychological cues in the content, detecting persuasion tactics, emotional manipulation, and ideological triggers commonly used by threat actors in cyber warfare.

### 5️⃣ **Attribution & Threat Actor Identification**

PolygraphGPT compares the identified patterns with known **APT groups** (e.g., Russian GRU, Iranian hackers), and uses **geopolitical timing**, **platform usage**, and **linguistic markers** to provide real-time attribution.

### 6️⃣ **Real-Time Research and Deep Mapping**

The system pulls in additional information from **Perplexity Sonar API**, scanning the web, news outlets, and security databases to cross-reference the detected patterns with ongoing campaigns and known TTPs. This helps create a **real-time attribution map**.

---

## 🧰 **Modules and SQL Database**

### **SQL Database Structure**:
PolygraphGPT stores data such as text samples, attribution results, and threat actor profiles in a **SQL database**. The database includes tables for:

- **Threat Actors**: Stores profiles of known groups and their tactics.
- **Influence Campaigns**: Logs detected campaigns, including metadata like date, platform, and affected region.
- **Linguistic Features**: Stores analyzed linguistic patterns and cognitive fingerprints.

### **Key Tables**:
- **Campaigns**: `campaign_id, title, description, detected_on, attributed_to`
- **Threat_Actors**: `actor_id, name, tactics, ideologies, known_targets`
- **Linguistic_Patterns**: `pattern_id, description, type, date_detected, source`
- **Deceptive_Content**: `content_id, text, media_type, detected_manipulation_type`

### **SQL Queries**:
PolygraphGPT uses **SQL queries** to analyze trends, detect recurring threat actor behavior, and fetch relevant data from the database. Example queries include:

- Retrieving known tactics from threat actors based on the detected manipulation in a piece of content.
- Querying the **Deceptive_Content** table to fetch all detected manipulated content of a specific type (e.g., deepfakes or phishing emails).

---

## 🛠️ **Built With**

- **Sonar API Features**:
  - 🔎 Real-Time Search
  - 🔗 Trusted Citations
  - 🧠 Chain-of-Thought Reasoning
  - 📚 Deep Research Mode

- **Tools**:
  - React.js
  - Flask + Python
  - MongoDB
  - Tailwind CSS

---

## 🎥 **Demo Video**

Watch how PolygraphGPT diagnoses and fixes issues:
➡️ [Demo Video Link](https://youtu.be/your-demo-link)

---

## 🧑‍💻 **Code Repository**

Link to the code repository will be added here.

---

## ✅ **Submission Checklist**

- [x] **Demo video** (max 3 mins)
- [x] **Code repo shared** with judges
- [x] **Detailed README** (this file)
- [x] **Perplexity API explanation** included
- [x] **Devpost form completed**

---

## 🗺️ **Future Roadmap**

- **Cyber Threat Diagnostics**: Add ability to detect malware-related symptoms.
- **Fintech Device Support**: Expand bot to help fix point-of-sale and fintech devices.
- **Multilingual Support**: Help users troubleshoot in multiple languages.
- **IT Ticket System Integration**: Sync bot with Zendesk, Freshdesk, etc.

---

## 👏 **Acknowledgments**

Thanks to **Perplexity AI** for Sonar API, which enabled real-time troubleshooting and research capabilities.  
Inspired by the daily struggles of users and IT teams trying to fix tech with limited guidance.

---

## 🛡️ **Let’s make tech troubleshooting smarter, faster, and user-friendly.**

**PolygraphGPT** — Your AI-powered IT helpdesk.

---
