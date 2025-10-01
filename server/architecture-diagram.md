# Arquitectura del Sistema RAG - Gemini/Ollama

## Diagrama de Arquitectura General

```mermaid
graph TB
    %% Cliente
    Client[🌐 Cliente Web/API]
    
    %% API Layer
    subgraph API["🚀 API Layer (FastAPI)"]
        GenerateEndpoint["/generate<br/>📝 Actividades Educativas"]
        StudentEndpoint["/generate/student<br/>🎓 Asistente Educativo"]
        DocumentsEndpoint["/documents/upload<br/>📄 Subida de Documentos"]
    end
    
    %% Services Layer
    subgraph Services["⚙️ Services Layer"]
        GenerateService[generate_response<br/>🔄 Lógica de Generación]
        AssistantService[generate_response_assistant<br/>🤖 Asistente Virtual]
        DocumentsService[upload_document<br/>📂 Procesamiento de Docs]
    end
    
    %% Core Layer
    subgraph Core["🔧 Core Layer"]
        ModelsCore[models.py<br/>🧠 LLM Integration]
        DocumentsCore[documents.py<br/>📚 Gestión de Documentos]
        VectorCore[vectorstore.py<br/>🔍 Vector Database]
    end
    
    %% AI Models
    subgraph AIModels["🤖 AI Models"]
        Gemini[Google Gemini 2.0<br/>🌟 Modelo Principal]
        Ollama[Ollama<br/>🦙 Modelo Local]
        OllamaStudent[medicina_usuario<br/>👨‍🎓 Modelo Estudiante]
    end
    
    %% Templates & Config
    subgraph Config["⚙️ Configuration"]
        CustomTemplate[custom_template<br/>📋 Plantilla Educativa]
        UserTemplate[user_template<br/>🎯 Plantilla Asistente]
        ConfigFile[config.py<br/>🔧 Configuración]
        EnvFile[.env<br/>🔐 Variables de Entorno]
    end
    
    %% Data Storage
    subgraph Storage["💾 Data Storage"]
        ChromaDB[(ChromaDB<br/>🔍 Vector Database)]
        Documents[(Documents<br/>📁 PDF/DOCX Files)]
        Logs[(Logs<br/>📊 Sistema de Logs)]
    end
    
    %% Utils
    subgraph Utils["🛠️ Utilities"]
        Filters[filters.py<br/>🧹 Filtros de Texto]
        Logging[logging.py<br/>📝 Sistema de Logs]
        Probability[probability.py<br/>📈 Cálculo de Similitud]
    end
    
    %% External Services
    subgraph External["🌍 External Services"]
        GoogleAPI[Google AI API<br/>🔗 Gemini Access]
        OllamaAPI[Ollama API<br/>📡 Local LLM Server]
    end
    
    %% Conexiones principales
    Client --> API
    
    %% API to Services
    GenerateEndpoint --> GenerateService
    StudentEndpoint --> AssistantService
    DocumentsEndpoint --> DocumentsService
    
    %% Services to Core
    GenerateService --> ModelsCore
    GenerateService --> DocumentsCore
    AssistantService --> ModelsCore
    DocumentsService --> DocumentsCore
    DocumentsService --> VectorCore
    
    %% Core to Storage and External
    ModelsCore --> AIModels
    DocumentsCore --> ChromaDB
    DocumentsCore --> Documents
    VectorCore --> ChromaDB
    
    %% AI Models to External APIs
    Gemini --> GoogleAPI
    Ollama --> OllamaAPI
    OllamaStudent --> OllamaAPI
    
    %% Configuration
    ModelsCore --> Config
    Core --> Utils
    
    %% Logging
    API --> Logs
    Services --> Logs
    Core --> Logs
    
    %% Styling
    classDef apiStyle fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef serviceStyle fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef coreStyle fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef aiStyle fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef storageStyle fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef configStyle fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    classDef utilStyle fill:#e0f2f1,stroke:#004d40,stroke-width:2px
    classDef extStyle fill:#fafafa,stroke:#424242,stroke-width:2px
    
    class API apiStyle
    class Services serviceStyle
    class Core coreStyle
    class AIModels aiStyle
    class Storage storageStyle
    class Config configStyle
    class Utils utilStyle
    class External extStyle
```

## Flujo de Datos Detallado

### 1. Generación de Actividades Educativas

```mermaid
sequenceDiagram
    participant C as Cliente
    participant GE as /generate Endpoint
    participant GS as GenerateService
    participant DC as DocumentsCore
    participant MC as ModelsCore
    participant VS as VectorStore
    participant AI as LLM (Gemini/Ollama)
    
    C->>GE: POST /generate (GenerateRequest)
    GE->>GS: generate_response()
    
    %% Recuperación de documentos
    GS->>DC: retrieve_docs(unidad, materia)
    DC->>VS: similarity_search()
    VS-->>DC: documentos relevantes
    DC-->>GS: context
    
    %% Generación con IA
    loop Máximo 3 intentos
        GS->>MC: generate_response_stream()
        MC->>AI: stream request + context
        AI-->>MC: chunks de respuesta
        MC-->>GS: respuesta completa
        
        %% Verificación de duplicados
        GS->>DC: retrieve_questions()
        DC->>VS: similarity_search(pregunta)
        VS-->>DC: preguntas similares + score
        DC-->>GS: similarity score
        
        alt score < 70% (única)
            GS->>DC: index_questions()
            DC->>VS: add_documents()
            GS-->>GE: respuesta final
        else score >= 70% (duplicada)
            Note over GS: Agregar a lista de preguntas previas
        end
    end
    
    GE-->>C: GenerateResponse
```

### 2. Asistente Virtual para Estudiantes

```mermaid
sequenceDiagram
    participant C as Cliente
    participant SE as /student Endpoint
    participant AS as AssistantService
    participant MC as ModelsCore
    participant AI as LLM (Modelo Estudiante)
    
    C->>SE: POST /student (RequestStudent)
    SE->>AS: generate_response_assistant()
    AS->>MC: generate_response_student()
    
    alt Modelo = "OLLAMA"
        MC->>AI: chat(model_student, messages)
        AI-->>MC: chunks de respuesta
    else Modelo = "GEMINI"
        MC->>AI: chain.stream(contexto, pregunta)
        AI-->>MC: chunks de respuesta
    end
    
    MC-->>AS: chunks
    AS->>AS: join chunks to full_response
    AS-->>SE: respuesta completa
    SE-->>C: respuesta del asistente
```

### 3. Subida y Procesamiento de Documentos

```mermaid
sequenceDiagram
    participant C as Cliente
    participant DE as /documents/upload
    participant DS as DocumentsService
    participant DC as DocumentsCore
    participant VS as VectorStore
    participant FS as FileSystem
    
    C->>DE: POST /upload (file, subject)
    DE->>DS: upload_document()
    DS->>FS: save file to disk
    
    DS->>DC: load_document()
    alt PDF
        DC->>DC: PDFPlumberLoader.load()
    else DOCX
        DC->>DC: Docx2txtLoader.load()
    end
    DC-->>DS: documents
    
    DS->>DC: index_docs()
    DC->>DC: split_documents()
    DC->>VS: add_documents()
    DC->>VS: persist()
    
    DS-->>DE: UploadResponse
    DE-->>C: resultado de la subida
```

## Componentes Clave

### Templates de Prompts

```mermaid
graph LR
    subgraph Templates["📋 Sistema de Templates"]
        CT[custom_template<br/>🎯 Generación de Actividades]
        UT[user_template<br/>🤖 Asistente Virtual]
        
        CT --> |Usado por| Generate[generate_response_stream]
        UT --> |Usado por| Student[generate_response_student]
    end
    
    subgraph Features["✨ Características"]
        AT[Tono Educativo<br/>📚]
        AR[Anti-Repetición<br/>🔄]
        JS[Formato JSON<br/>📝]
        EM[Empático y Paciente<br/>💙]
    end
    
    CT --> AT
    CT --> AR  
    CT --> JS
    UT --> EM
    UT --> JS
```

### Sistema de Vector Database

```mermaid
graph TB
    subgraph VectorDB["🔍 ChromaDB Vector Storage"]
        MC[Materia Collections<br/>📚 Documentos por materia]
        QC[Question Collections<br/>❓ Preguntas generadas]
        
        subgraph Embeddings["🔤 Embeddings"]
            NE[nomic-embed-text<br/>🦙 Ollama Embeddings]
        end
    end
    
    subgraph Operations["⚙️ Operaciones"]
        SS[Similarity Search<br/>🔍 Búsqueda semántica]
        AD[Add Documents<br/>➕ Indexación]
        RD[Retrieve Docs<br/>📖 Recuperación]
    end
    
    MC --> SS
    QC --> SS
    NE --> MC
    NE --> QC
    SS --> RD
    AD --> MC
    AD --> QC
```

### Configuración y Variables de Entorno

```mermaid
graph LR
    subgraph EnvConfig["🔧 Configuración"]
        ENV[.env<br/>🔐 Variables de Entorno]
        CONFIG[config.py<br/>⚙️ Configuración Central]
    end
    
    subgraph Variables["📊 Variables Principales"]
        MODEL[MODEL<br/>🤖 GEMINI/OLLAMA]
        API_KEY[API_KEY<br/>🔑 Google AI]
        OLLAMA_URL[OLLAMA_URL<br/>🌐 Servidor Local]
        MODEL_STUDENT[MODEL_USER_OLLAMA<br/>👨‍🎓 Modelo Estudiante]
    end
    
    ENV --> CONFIG
    CONFIG --> MODEL
    CONFIG --> API_KEY
    CONFIG --> OLLAMA_URL
    CONFIG --> MODEL_STUDENT
```

## Patrones Arquitectónicos Implementados

1. **🏗️ Layered Architecture**: API → Services → Core → Storage
2. **🔄 Repository Pattern**: Abstracción de acceso a datos
3. **🎯 Strategy Pattern**: Intercambio entre Gemini y Ollama
4. **📋 Template Method**: Reutilización de lógica de generación
5. **🔍 RAG (Retrieval-Augmented Generation)**: Enriquecimiento contextual
6. **📊 Logging Pattern**: Trazabilidad completa de operaciones
7. **⚡ Streaming Pattern**: Respuestas en tiempo real

## Tecnologías Utilizadas

- **🚀 FastAPI**: Framework web asíncrono
- **🦜 LangChain**: Orquestación de LLMs
- **🔍 ChromaDB**: Base de datos vectorial
- **🌟 Google Gemini 2.0**: Modelo de IA principal
- **🦙 Ollama**: Servidor de modelos locales
- **📄 PDFPlumber/Docx2txt**: Procesamiento de documentos
- **🔤 Nomic Embed**: Embeddings de texto
- **📝 Pydantic**: Validación de datos
- **📊 Python Logging**: Sistema de logs
