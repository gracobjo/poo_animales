# Modelos UML — Refugio Animal

Diagramas UML habituales aplicados a `tarea1/` (Mermaid).

| Tipo | Sección |
| --- | --- |
| Clases, componentes, despliegue, objetos | [1. Estructurales](#1-diagramas-estructurales-estáticos) |
| Casos de uso, secuencia, actividades | [2. Comportamiento](#2-diagramas-de-comportamiento-dinámicos) |

Catálogo narrativo de CU: [casos_de_uso.md](casos_de_uso.md).

---

## 1. Diagramas estructurales (estáticos)

### 1.1 Diagrama de clases

El **CRUD** usa un **diccionario** (`RegistroAnimal`). En paralelo, capa POO Tema 2: `AnimalRefugio` y subclases. UI: `GestorAnimales`, `DialogoFichaClinica`.

```mermaid
classDiagram
  direction TB

  class AnimalRefugio {
    <<abstract>>
    +ESPECIE: str
    -_nombre
    -_edad
    -_peso
    -_color
    -_observaciones
    +nombre: str
    +edad: int
    +peso: float
    +color: str
    +observaciones: str
    +especie: str
    +info_basica()* str
    +hacer_sonido()* str
    +tipo_alimentacion()* str
    +campos_desde_dict()$ dict
  }

  class Perro {
    +ESPECIE = Perro
    +hacer_sonido()
    +tipo_alimentacion()
  }
  class Gato {
    +ESPECIE = Gato
    +hacer_sonido()
    +tipo_alimentacion()
  }
  class Conejo {
    +ESPECIE = Conejo
    +hacer_sonido()
    +tipo_alimentacion()
  }
  class Loro {
    +ESPECIE = Loro
    +hacer_sonido()
    +tipo_alimentacion()
  }
  class Hamster {
    +ESPECIE = Hámster
    +hacer_sonido()
    +tipo_alimentacion()
  }

  AnimalRefugio <|-- Perro
  AnimalRefugio <|-- Gato
  AnimalRefugio <|-- Conejo
  AnimalRefugio <|-- Loro
  AnimalRefugio <|-- Hamster

  class AdaptadorPoo {
    <<module>>
    +registro_a_animal()
    +animal_a_campos()
    +resumen_polimorfico()
  }

  AdaptadorPoo ..> AnimalRefugio : crea

  class ESPECIES {
    <<enumeration>>
    Perro
    Gato
    Conejo
    Loro
    Hámster
  }

  class Tratamiento {
    +str fecha
    +str descripcion
    +str veterinario
  }

  class Vacunacion {
    +str fecha
    +str vacuna
    +str proxima
  }

  class Documento {
    +str nombre
    +str ruta
    +str fecha
  }

  class RegistroAnimal {
    <<dict>>
    +str nombre
    +str especie
    +int edad
    +float peso
    +str color
    +str observaciones
    +str foto
    +Tratamiento[] tratamientos
    +Vacunacion[] vacunaciones
    +Documento[] documentos
  }

  class Inventario {
    <<Dict~int,RegistroAnimal~>>
    +animales_iniciales() Inventario
    +crear_animal(datos, inv) int
    +leer_animal(id, inv) RegistroAnimal
    +actualizar_animal(id, datos, inv)
    +borrar_animal(id, inv) RegistroAnimal
  }

  class Adjuntos {
    <<module>>
    +TAMANO_MAX_BYTES
    +importar_archivo()
    +registrar_documento()
    +registrar_foto()
    +guardar_bytes()
  }

  class validar_datos {
    <<function>>
    +validar_datos(datos) RegistroAnimal
  }

  class GestorAnimales {
    -inventario
    -lbl_foto
    +_crear()
    +_actualizar()
    +_borrar()
    +_seleccionar()
    +_exportar_pdf()
    +_abrir_ficha_clinica()
    +_mostrar_foto_formulario()
  }

  class DialogoFichaClinica {
    -animal_id
    -registro
    +_add_tratamiento()
    +_importar_doc()
    +_pegar_doc()
    +_importar_foto()
    +_pegar_foto()
  }

  class ExportacionPDF {
    <<module>>
    +exportar_fichas_pdf()
  }

  class App {
    +main()
  }

  Inventario "1" *-- "*" RegistroAnimal
  RegistroAnimal *-- "*" Tratamiento
  RegistroAnimal *-- "*" Vacunacion
  RegistroAnimal *-- "*" Documento
  RegistroAnimal --> ESPECIES
  Inventario ..> validar_datos
  GestorAnimales --> Inventario
  GestorAnimales --> DialogoFichaClinica : abre
  GestorAnimales ..> ExportacionPDF
  DialogoFichaClinica --> Adjuntos
  DialogoFichaClinica --> RegistroAnimal : muta
  ExportacionPDF ..> RegistroAnimal
  App ..> GestorAnimales
  App ..> Inventario
```

---

### 1.2 Diagrama de componentes

```mermaid
flowchart TB
  subgraph UI["interfaz"]
    GESTOR[gestor.py]
    CLIN[ficha_clinica.py]
    EST[estilos.py]
    FOTO[vista_foto.py]
    CLIP[portapapeles.py]
  end

  subgraph DOM["datos"]
    INV[inventario.py]
    FIC[ficha.py]
    ADJ[adjuntos.py]
    CON[constantes.py]
  end

  subgraph VAL["validaciones"]
    REG[reglas.py]
  end

  subgraph EXP["exportacion"]
    PDF[pdf_fichas.py]
  end

  subgraph EXT["externo"]
    TK[tkinter]
    FPDF[fpdf2]
    PIL[Pillow]
    FS[adjuntos/ en disco]
    MUE[muestras/]
  end

  APP[app.py] --> GESTOR
  APP --> INV
  GESTOR --> CLIN
  GESTOR --> INV
  GESTOR --> PDF
  GESTOR --> FOTO
  GESTOR --> EST
  GESTOR --> TK
  CLIN --> ADJ
  CLIN --> CLIP
  CLIN --> FOTO
  CLIP --> PIL
  CLIP --> TK
  INV --> REG
  REG --> CON
  ADJ --> FS
  PDF --> FPDF
  PDF --> PIL
  CLIN -.-> MUE
```

---

### 1.3 Diagrama de despliegue

```mermaid
flowchart TB
  subgraph PC["Nodo: PC del operario"]
    subgraph RT["Runtime"]
      PY[Python 3.8+]
      TKRT[Tk / Tcl]
    end
    subgraph ART["Artefactos"]
      APP[app.py + paquetes]
      MEM[Inventario en RAM]
      DISK[adjuntos/id/fotos|documentos]
      OUT[PDF exportado]
    end
    APP --> PY
    APP --> TKRT
    APP --> MEM
    APP --> DISK
    APP --> OUT
  end
  Op([Operario]) -->|GUI| APP
```

---

### 1.4 Diagrama de objetos (arranque)

```mermaid
flowchart LR
  inv[(inventario)]
  l1["1 Luna Perro\nvacuna Rabia\ntrat. desparasitación"]
  l2["2 Misi Gato"]
  l3["3 Kiko Loro"]
  l4["4 Toby Perro"]
  inv --> l1 & l2 & l3 & l4
  gui[GestorAnimales]
  gui --> inv
```

Tras pegar un PDF a Luna: `documentos[0].ruta = adjuntos/1/documentos/...`.

---

## 2. Diagramas de comportamiento (dinámicos)

### 2.1 Casos de uso (compacto)

```mermaid
flowchart LR
  U([Operario])
  U --- UC01 & UC04 & UC05 & UC09 & UC10 & UC11 & UC12
```

Detalle: [casos_de_uso.md](casos_de_uso.md).

---

### 2.2 Secuencia — crear animal

```mermaid
sequenceDiagram
  actor Op as Operario
  participant G as GestorAnimales
  participant C as crear_animal
  participant V as validar_datos
  participant I as inventario

  Op->>G: Crear
  G->>G: _datos_del_formulario()
  G->>C: crear_animal(datos, inv)
  C->>V: validar_datos(datos)
  V-->>C: registro
  C->>I: inv[nuevo_id]=registro
  C-->>G: nuevo_id
  G->>G: _actualizar_tabla + _limpiar
```

---

### 2.3 Secuencia — pegar documento

```mermaid
sequenceDiagram
  actor Op as Operario
  participant D as DialogoFichaClinica
  participant P as leer_portapapeles
  participant A as registrar_documento
  participant FS as adjuntos/

  Op->>D: Pegar / Ctrl+V
  D->>P: leer_portapapeles()
  alt CF_HDROP / ruta
    P-->>D: archivos
    D->>A: registrar_documento(id, ruta)
    A->>A: comprobar_tamano ≤ 5 MB
    A->>FS: copy2
  else texto
    D->>A: registrar_documento_bytes(.txt)
  else imagen
    D->>A: registrar_documento_bytes(.png)
  else vacío / error
    D-->>Op: showerror
  end
  A-->>D: entrada
  D->>D: refrescar lista
```

---

### 2.4 Secuencia — exportar PDF con foto

```mermaid
sequenceDiagram
  actor Op as Operario
  participant G as GestorAnimales
  participant E as exportar_fichas_pdf
  participant PDF as PdfFichas

  Op->>G: Exportar PDF
  G->>G: ids seleccionados o visibles
  G->>E: exportar_fichas_pdf(inv, ruta, ids)
  E->>PDF: página + campos + clínica
  opt hay foto
    E->>PDF: image(miniatura)
  end
  PDF-->>E: output
  E-->>G: total
  G-->>Op: showinfo
```

---

### 2.5 Actividades — adjunto (importar/pegar)

```mermaid
flowchart TD
  start([Inicio]) --> origen{¿Origen?}
  origen -->|Importar| dlg[Diálogo de archivo]
  origen -->|Pegar| clip[Leer portapapeles]
  dlg --> tam{¿≤ 5 MB?}
  clip --> tipo{¿Tipo?}
  tipo -->|archivos| tam
  tipo -->|imagen/texto| bytes[Serializar a bytes]
  bytes --> tam2{¿≤ 5 MB?}
  tam -->|No| err[Error]
  tam2 -->|No| err
  tam -->|Sí| copy[Copiar a adjuntos/id/...]
  tam2 -->|Sí| copy
  copy --> ui[Actualizar lista / foto]
  ui --> fin([Fin])
  err --> fin
```

---

### 2.6 Actividades — filtrar tabla

```mermaid
flowchart TD
  s([Cambio búsqueda/filtro]) --> clear[Vaciar Treeview]
  clear --> loop[Para cada ficha]
  loop --> ok{¿Nombre y especie OK?}
  ok -->|Sí| ins[Insertar fila]
  ok -->|No| next[Siguiente]
  ins --> next
  next --> more{¿Más?}
  more -->|Sí| loop
  more -->|No| st[Actualizar estado]
```

---

## 3. Uso en la defensa

| Pregunta | Diagrama |
| --- | --- |
| ¿Cómo está el código? | Componentes / clases |
| ¿Dónde corre? | Despliegue |
| ¿Qué puede hacer el usuario? | Casos de uso |
| ¿Qué pasa al pegar / exportar? | Secuencia |
| ¿Pasos y bifurcaciones? | Actividades |
| ¿Cómo se ven los datos al inicio? | Objetos |

Código de referencia: `interfaz/gestor.py`, `ficha_clinica.py`, `portapapeles.py`, `datos/adjuntos.py`, `exportacion/pdf_fichas.py`.
