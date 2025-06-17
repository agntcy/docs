# Agent Directory Record Example

## Skill Tags (Taxonomy)
```yaml
├── analytical_skills
│   ├── analytical_skills
│   ├── coding_skills
│   │   ├── code_optimization
│   │   ├── code_templates
│   │   ├── code_to_docstrings
│   │   ├── coding_skills
│   │   └── text_to_code
│   └── mathematical_reasoning
│       ├── geometry
│       ├── math_word_problems
│       ├── mathematical_reasoning
│       ├── pure_math_operations
│       └── theorem_proving
├── audio
│   ├── audio_classification
│   ├── audio_to_audio
│   └── audio
├── base_skill
├── images_computer_vision
│   ├── depth_estimation
│   ├── image_classification
│   ├── image_feature_extraction
│   ├── image_generation
│   ├── image_segmentation
│   ├── image_to_3d
│   ├── image_to_image
│   ├── images_computer_vision
│   ├── keypoint_detection
│   ├── mask_generation
│   ├── object_detection
│   └── video_classification
├── multi_modal
│   ├── any_to_any
│   ├── audio_processing
│   │   ├── audio_processing
│   │   ├── speech_recognition
│   │   └── text_to_speech
│   ├── image_processing
│   │   ├── image_processing
│   │   ├── image_to_text
│   │   ├── text_to_3d
│   │   ├── text_to_image
│   │   ├── text_to_video
│   │   └── visual_qa
│   └── multi_modal
├── nlp
│   ├── analytical_reasoning
│   │   ├── analytical_reasoning
│   │   ├── fact_verification
│   │   ├── inference_deduction
│   │   └── problem_solving
│   ├── creative_content
│   │   ├── creative_content
│   │   ├── poetry_writing
│   │   └── storytelling
│   ├── ethical_interaction
│   │   ├── bias_mitigation
│   │   ├── content_moderation
│   │   └── ethical_interaction
│   ├── feature_extraction
│   │   ├── feature_extraction
│   │   └── model_feature_extraction
│   ├── information_retrieval_synthesis
│   │   ├── document_passage_retrieval
│   │   ├── fact_extraction
│   │   ├── information_retrieval_synthesis
│   │   ├── knowledge_synthesis
│   │   ├── question_answering
│   │   ├── search
│   │   └── sentence_similarity
│   ├── language_translation
│   │   ├── language_translation
│   │   ├── multilingual_understanding
│   │   └── translation
│   ├── natural_language_generation
│   │   ├── dialogue_generation
│   │   ├── nlg
│   │   ├── paraphrasing
│   │   ├── question_generation
│   │   ├── story_generation
│   │   ├── style_transfer
│   │   ├── summarization
│   │   └── text_completion
│   ├── natural_language_understanding
│   │   ├── contextual_comprehension
│   │   ├── entity_recognition
│   │   ├── nlu
│   │   └── semantic_understanding
│   ├── nlp
│   ├── personalization
│   │   ├── personalization
│   │   ├── style_adjustment
│   │   └── user_adaptation
│   ├── text_classification
│   │   ├── natural_language_inference
│   │   ├── sentiment_analysis
│   │   ├── text_classification
│   │   └── topic_labeling
│   └── token_classification
│       ├── named_entity_recognition
│       ├── pos_tagging
│       └── token_classification
├── retrieval_augmented_generation
│   ├── document_or_database_question_answering
│   ├── generation_of_any
│   ├── retrieval_augmented_generation
│   └── retrieval_of_information
│       ├── document_retrieval
│       ├── indexing
│       ├── retrieval_of_information
│       └── search
└── tabular_text
    ├── tabular_classification
    ├── tabular_regression
    └── tabular_text
```

## Record Examples without Digests (Content Identifier)

### Email Reviewer AI Agent
```json
{
  "name": "agntcy/email_reviewer",
  "skills": [
    {
      "class_uid": 10101,
      "class_name": "Contextual Comprehension",
      "category_uid": 1,
      "category_name": "Natural Language Processing"
    },
    {
      "class_uid": 10206,
      "class_name": "Text Style Transfer",
      "category_uid": 1,
      "category_name": "Natural Language Processing"
    },
    {
      "class_uid": 10602,
      "class_name": "Tone and Style Adjustment",
      "category_uid": 1,
      "category_name": "Natural Language Processing"
    },
    {
      "class_uid": 10702,
      "class_name": "Problem Solving",
      "category_uid": 1,
      "category_name": "Natural Language Processing"
    },
    {
      "class_uid": 10203,
      "class_name": "Text Paraphrasing",
      "category_uid": 1,
      "category_name": "Natural Language Processing"
    },
    {
      "class_uid": 10303,
      "class_name": "Knowledge Synthesis",
      "category_uid": 1,
      "category_name": "Natural Language Processing"
    }
  ],
  "authors": [
    "Cisco Systems Inc."
  ],
  "version": "v1.0.0",
  "locators": [
    {
      "url": "https://github.com/agntcy/agentic-apps/tree/main/email_reviewer",
      "type": "source-code"
    },
    {
      "url": "https://github.com/agntcy/agentic-apps/tree/main/email_reviewer/pyproject.toml",
      "type": "python-package"
    }
  ],
  "signature": {
    "algorithm": "SHA2_256",
    "signature": "MEUCIQCIlAthHnRAOeHqVqVvy/KW2xej6nTPdsnpmSmHyDoExAIgbl2j/2dFr6oGAdUJG[...]",
    "signed_at": "2025-05-21T16:43:35+02:00",
    "certificate": "MIICzjCCAlWgAwIBAgIUfTQ0MzM0WhI[...]",
    "content_type": "application/vnd.dev.sigstore.bundle.v0.3+json",
    "content_bundle": "eyJtZWRpYVR5cGUiOiJhcHBsaWNhdGlvbi92bm0lCQWd [...]"
  },
  "created_at": "2025-04-24T12:00:00Z",
  "extensions": [
    {
      "data": {
        "sbom": {
          "name": "email_reviewer",
          "packages": [
            {
              "name": "dotenv",
              "version": "^0.9.9"
            },
            {
              "name": "llama-index-core",
              "version": "^0.12.30"
            },
            {
              "name": "llama-index-llms-azure-openai",
              "version": "^0.3.1"
            },
            {
              "name": "agntcy_acp",
              "version": "v0.1.0a2"
            }
          ]
        }
      },
      "name": "schema.oasf.agntcy.org/features/runtime/framework",
      "version": "v0.0.0"
    },
    {
      "data": {
        "type": "python",
        "version": ">=3.9,<4.0"
      },
      "name": "schema.oasf.agntcy.org/features/runtime/language",
      "version": "v0.0.0"
    }
  ],
  "annotations": {
    "type": "llama-index"
  },
  "description": "Agent in charge of reviewing and correcting emails addressed to a specific audience.",
  "schema_version": "v0.3.1"
}
```

The content identifier of the record is a SHA-256 hash digests which makes it

- Globally unique
- Content-addressable
- Collision-resistant
- Immutable