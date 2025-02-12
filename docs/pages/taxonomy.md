# Taxonomy of tasks

Here we present a taxonomy of tasks for LLM agents. We start by discussing
global tasks, based on <https://huggingface.co/tasks>. We complete that overview
with a taxonomy of some specialized tasks, more relevant for Cisco. We finish by
providing a very detailed taxonomy of tasks related to NetOPS, which is most
relevant for Cisco.

## Taxonomy of Global Tasks

| Task    | Subtasks |
| -------- | ------- |
| Natural Language Processing  | Question Answering    |
|  | Summarization |
|  | Translation |
|  | Text Generation |
|  | Text Classification |
|  | Table Question Answering |
|  | Zero-Shot Classification |
|  | Sentence Similarity |
|  | Feature Extraction |
|  | Fill-Mask |
|  | Token Classification |
| Computer Vision | Image Classification |
|  |  Image Feature Extraction |
|  |  Image Segmentation |
|  |  Video Classification |
|  |  Text-to-Image |
|  |  Text-to-Video |
|  |  Image-to-Image |
|  |  Image-to-Text |
|  |  Keypoint Detection |
|  |  Mask Generation |
|  |  Object Detection |
|  |  Depth Estimation |
|  |  Unconditional Image Generation |
|  |  Zero-Shot Image Classification |
|  |  Zero-Shot Object Detection |
|  |  Text-to-3D |
|  |  Image-to-3D |
| Audio | Audio Classification  |
|  |   Audio-to-Audio  |
|  |   Automatic Speech Recognition  |
|  |   Text-to-Speech |
| Multimodal |   Contribute Audio-Text-to-Text |
|  |   Contribute Document Question Answering |
|  |   Image-Text-to-Text |
|  |   Video-Text-to-Text |
|  |   Visual Question Answering |
|  |   Any-to-Any |

## Taxonomy of Specialized Tasks

Here we give a taxonomy of some more specialized tasks, relevant to Cisco. For
each task, we give an appreciation of the research community's progress on it,
some example metrics and explain how hard it is to evaluate the task.

| Task | Subtasks | Progress | Metrics | Hardness to evaluate |
| - | - | - | -| :- |
| Natural<br> Language<br> Processing |  | Advanced  | Next-word-<br>prediction.<br> Cloze tasks.<br> Otherwise more<br> ambiguous. | If task can be<br> rephrased as<br> next-word-prediction,<br> performance is known.<br> Otherwise more<br> ambiguous.|
|  |   Natural language<br> understanding   |  |  |  |
|  |   Reasoning                        |  |  |  |
|  |   Natural language<br> generation      |  |  |  |
|  |   Multi-lingual                    |  |  |  |
| Retrieval<br> augmented<br> generation |  | Medium<br> (search needs<br> improvement).  | Context<br> relevance.<br> Answer<br> relevance.<br> Faithfullness.<br> Retriever quality. | Rather difficult,<br> as there are <br>multiple aspects.<br> Quality of <br>generated text is<br> usually evaluated<br> with another LLM <br>- which is shabby. |
|  |   Retrieval of <br>information   |  |  |  |
|  |  Generation of <br>output |  |  |  |
| Coding | | Medium.<br> The models<br> are not<br> sample-efficient.<br> Syntactically <br>incorrect<br> or undefined<br> code.<br> Degradation with<br> docstring length<br> and number of<br> building blocks. | Pass rate on<br> unit-tests.<br> Execution <br> accuracy.<br> Compilation <br> accuracy. | Rather straight<br> forward. |
|   |   Translating natural<br> language into<br> code   |  |  |  |
|  |  Translation code into<br> docstrings |  |  |  |
|  |  Filling in code<br> templates |  |  |  |
|  |  Refactoring and <br>optimising existing<br> code |  |  |  |
| Mathematical<br> reasoning | | Early stages.<br> Mixing words and<br> numbers is hard.<br> Probabilistic nature<br> of LLMs contradicts<br> deterministic<br> answers. | Exact solution<br> to problems| Rather straight <br>forward, <br> except for theorem <br>proving etc. |
|  |  Pure Mathematical<br> Operations   |  |  |  |
|  |  Math Word<br> Problems |  |  |  |
|  |  Geometry |  |  |  |
|  |  Automated Theorem<br> Proving |  |  |  |

## Taxonomy of NetOPS Tasks

Here we discuss tasks related to Network Operations (NetOPS). We distinguish at
least five global tasks that can be done using LLMs:

* Answering NetOPS knowledge questions (e.g., What is the order of bandwidth
  measurement from smallest to largest?);
* Generate a query on a dataset (e.g., produce Python code to filter a pandas
  Dataframe);
* Retrieval Augmented Generation, where the database contains information about
  components of a network (e.g., a knowledge base, log collection, ticketing
  system);
* Orchestration of multiple agents and/or tools, where a LLM takes in a prompt
  and decides what action to take (e.g., call upon an agent to inspect a
  database, another one to do data analysis, etc.). Examples:
  * Network monitoring;
  * Network topology planning;
  * Network device management;
  * Network troubleshooting;
  * Network performance optimisation;
  * Network security.
  * Network backup and recovery;
* Network engineering (overlapping with the previous task):
  * Network Design and Planning;
  * Network Implementation;
  * Network Analytics;
  * Network Management.

### Tasks from Network Engineering

A rather up-to-date review of LLMs used in the context of network engineering
can be found in [Large Language Models Meet Next-Generation Networking
Technologies: A Review](https://www.mdpi.com/1999-5903/16/10/365). We distill
here the four categories of network engineering tasks, together with the cited
works on specific subtasks. References are with respect to this review.  

#### Network Design and Planning

| Subtasks | Work | Baseline Model(s) |
| -------- | ------- | ------- |
| Load Balancing, <br> Capacity Planning | Desai et al. [133] | GPT-4 |
| Intent-Based Networking, <br> Telecommunications, 6G,<br> Network Energy Saving | Zou et al. [130] | GPT-4|
| QoE, <br> Bandwidth Management, <br> Job Scheduling, <br> Adaptive Bitrate Streaming | NetLLM [129] | LLaMA 2 |
| QoS, <br> Network Provisioning, <br> Cloud-Edge Resource Allocation and Scheduling | NetGPT [134] | GPT-2,<br> LLaMA |
| QoS, <br> Network Service Recommendation | llmQoS [132] | RoBERTa,<br> Phi-3 |
| QoE, <br> Power Scheduling, <br> Resource Allocation | Mongaillard et al. [131] | LLaMA 3,<br> GPT-4,<br> Gemini 1.5 |

References are w.r.t. [Large Language Models Meet Next-Generation Networking
Technologies: A Review](https://www.mdpi.com/1999-5903/16/10/365).

#### Network Implementation

| Subtasks | Work | Baseline Model(s) |
| -------- | ------- | ------- |
|Router Configuration | VPP [135] | GPT-4  |
|Configuration Validation | Ciri [136] | GPT-4,<br> GPT-3.5,<br> Claude 3,<br> Code Llama,<br> DeepSeek |
|Network Configuration | NETBUDDY [137] | GPT-4 |
|Intent-Based Networking,<br> Virtual Network Function,<br> Network Policy | Emergence [138] | GPT-4,<br> GPT-3.5 |
|Federated Learning | GPT-FL [139] | GPT-3 |
|Federated Learning | LP-FL [140] | BERT |
|Cybersecurity, Network Protocol | ChatAFL [141] | GPT-3.5 |
|Network Configuration,<br> Intent-Based Networking,<br> Next Generation Network,<br> Network Service Descriptor | Mekrache et al. [142] | Code Llama |
|Network Configuration,<br> Network Topology,<br> Intent-Based Networking | GeNet [143] | GPT-4 |
|Network Configuration,<br> Intent-Based Networking,<br> Network Digital Twin | S-Witch [144] | GPT-3.5 |
|Network Configuration,<br> Intent-Based Networking,<br> Next Generation Network | Mekrache et al. [145] | Code Llama |
|Network Configuration,<br> Intent-Based Networking | Fuad et al. [146] | GPT-4,<br> GPT-3.5,<br> LLaMA 2,<br> Mistral 7B |

References are w.r.t. [Large Language Models Meet Next-Generation Networking
Technologies: A Review](https://www.mdpi.com/1999-5903/16/10/365).

#### Network Analytics

| Subtasks | Work | Baseline Model(s) |
| -------- | ------- | ------- |
| Networking Text Classification and <br> Networking Information Retrieval | NetBERT [147] | BERT |
| Log Analysis,<br> Intrusion Detection | GPT-2C [148] | GPT-2 |
| Network Dynamics,<br> Network Traffic | NTT [149] | Vanilla Transformer |
| Log Analysis,<br> Anomaly Detection | LogGPT [150] | GPT-3.5 |
| Log Analysis,<br> Anomaly Detection | LAnoBERT [151] | BERT |
| Telecommunication,<br> Network Traffic,<br> Intent-Based Networking | NetLM [152] | GPT-4 |
| Log Analysis | BERTOps [153] | BERT |
| Log Analysis,<br> Anomaly Detection | LogGPT [154] | GPT-2 |
| Cybersecurity,<br> Vulnerability Detection | Szabó et al. [155] | GPT-3.5,<br> GPT-4  |
| Telecommunication | Piovesan et al. [156] | Phi-2 |
| Log Parsing,<br> Log Analysis | LILAC [157] | GPT-3.5 |
| Network Data Analytic Function,<br> Telecommunications,<br> 5G | Mobile-LLaMA [158] | LLaMA 2 |

References are w.r.t. [Large Language Models Meet Next-Generation Networking
Technologies: A Review](https://www.mdpi.com/1999-5903/16/10/365).

### Network Management

| Subtasks | Work | Baseline Model(s) |
| -------- | ------- | ------- |
| Cybersecurity,<br> Man-in-the-Middle Attack,<br> Internet of Things | Wong et al. [159] | DistilBERT |
| Cybersecurity | CyBERT [160] | BERT |
| Cybersecurity,<br> Malware Detection | MalBERT [161] |
| BERT Cybersecurity,<br> Cyber Threat Intelligence | SecureBERT [162] | BERT |
| Cybersecurity,<br> Malware Detection | Demırcı et al. [163] | GPT-2 |
| Network Monitoring,<br> Fully Qualified Domain Name | NorBERT [164] | BERT  |
| Cybersecurity,<br> Network Traffic | PAC-GPT [165] | GPT-3 |
| Network Incident Management | Hamadanian et al. [166] | GPT-4 |
| Information Security,<br> Log Parsing,<br> Anomaly Detection | Owl [167] | Vanilla Transformer |
| Network Lifecycle Management,<br> Network Traffic,<br> Program Synthesis | Mani et al. [168] | GPT-4,<br> GPT-3,<br> Text-davinci-003,<br> Google Bard |
| QoS,<br> Telecommunication | Bariah et al. [169] | GPT-2,<br> BERT,<br> DistilBERT,<br> RoBERTa |
| Cybersecurity | Tann et al. [170] | GPT-3.5,<br> PaLM 2,<br> Prometheus |
| Cybersecurity | Cyber Sentinel [171] | GPT-4 |
| Cybersecurity | Moskal et al. [172] | GPT-3.5 |
| Cybersecurity,<br> Network Protocol,<br> Man-in-the-Middle Attack | Net-GPT [173] | LLaMA 2,<br> DistilGPT-2 |
| Network Measurement,<br> Internet of Things | Sarabi et al. [174] | RoBERTa |
| Cybersecurity,<br> Anomaly Detection,<br> Intrusion Detection | HuntGPT [175] | GPT-3.5 |
| Cybersecurity | Zhang et al. [176] | GPT-2 |
| Cybersecurity,<br> Network Traffic,<br> Distributed Denial of Service Attack | ShieldGPT [177] | GPT-4 |
| Cybersecurity,<br> Cyber Threat Detection,<br> Internet of Things | SecurityBERT [178] | BERT  |
| Network Optimization,<br> Intent-Based Networking | Habib et al. [179] | ALBERT |
| Cybersecurity,<br> Distributed Denial of Service Attack | DoLLM [180] | LLaMA 2  |

References are w.r.t. [Large Language Models Meet Next-Generation Networking
Technologies: A Review](https://www.mdpi.com/1999-5903/16/10/365).
