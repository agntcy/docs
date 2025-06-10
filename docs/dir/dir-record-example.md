# Agent Directory Records Example

## Skill Tags (Taxonomy)
```yaml
skills:
  language:
    - text-generation
    - text-completion
    - text-summarization
    - text-translation
  vision:
    - image-generation
    - image-classification
    - object-detection
  audio:
    - speech-to-text
    - text-to-speech
  reasoning:
    - task-planning
    - decision-making
    - problem-solving
```

## Record Examples with Digests

### Text Generation Agent
```json
{
  "digest": "sha256:4e8c72f126b2e4a318911ba11b39432978d0611a56d53a2cfb6fdb42853df0e2",
  "skills": [
    "language/text-generation",
    "language/text-completion"
  ],
  "metadata": {
    "name": "gpt4-agent",
    "version": "1.0.0",
    "locator": {
      "type": "github",
      "url": "github.com/agntcy/agents/gpt4-agent"
    }
  }
}
```

### Vision Processing Agent
```json
{
  "digest": "sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
  "skills": [
    "vision/image-generation",
    "vision/image-classification"
  ],
  "metadata": {
    "name": "dall-e-agent",
    "version": "2.0.0",
    "locator": {
      "type": "github",
      "url": "github.com/agntcy/agents/dalle-agent"
    }
  }
}
```

### Multi-Modal Agent
```json
{
  "digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "skills": [
    "language/text-generation",
    "vision/image-generation",
    "reasoning/task-planning"
  ],
  "metadata": {
    "name": "multi-modal-agent",
    "version": "1.0.0",
    "locator": {
      "type": "github",
      "url": "github.com/agntcy/agents/multimodal-agent"
    }
  }
}
```

The digests are SHA-256 hashes of the record content, making them:

- Globally unique
- Content-addressable
- Collision-resistant
- Immutable