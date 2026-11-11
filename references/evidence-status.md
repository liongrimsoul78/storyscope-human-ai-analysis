# Estados de evidencia y regla de ausencia

Esta tabla es obligatoria. No se puede asignar dirección a un rasgo hasta registrar su estado.

| Estado | Significado | ¿Puede tener dirección? | Ejemplo |
|---|---|---|---|
| **Presente–alineado** | Un valor directamente observado coincide con la opción/dirección elevada en el corpus del estudio. | Sí | Una revelación genuina reinterpreta varias escenas previas: valor alineado con profundidad de recontextualización elevada en humanos. |
| **Presente–opuesto** | Un valor directamente observado es el polo alternativo de una característica que tiene una dirección en el estudio. | Sí; es contraevidencia real | Para `Reference Explicitness`, se observa principalmente una opción diferente de la que el estudio elevó para el grupo comparado. |
| **Ausente** | Se buscó la característica y no se halló; su ausencia no es por sí misma un valor direccional. | No, por defecto | No se encuentra una descripción olfativa en un texto breve. |
| **No aplicable** | El rasgo no corresponde al tipo de texto/género/tarea. | No | Subtramas en una etiqueta de producto o un formulario. |
| **No evaluable** | Longitud, fragmentariedad, falta de contexto o falta de oportunidad impide decidir. | No | No puede inferirse la presencia/ausencia de subtramas a partir de 21 palabras. |

## Regla de decisión

1. ¿Es posible inspeccionar la característica en el texto suministrado?
   - No → `No evaluable`.
2. ¿La característica tiene sentido para el género/tarea?
   - No → `No aplicable`.
3. ¿Hay un valor afirmativamente observable?
   - Sí → identificar el valor concreto y decidir `Presente–alineado`, `Presente–opuesto` o `neutral`, según la opción y la tabla publicada.
4. ¿No aparece?
   - Registrar `Ausente`; no asignar dirección salvo que la ausencia sea una categoría explícita del rasgo y el texto tenga longitud/completitud suficiente para sostener esa codificación.

## Diferencia entre ausencia y valor categórico “ninguno”

No son equivalentes:

- **Ausencia superficial:** no se menciona una subtrama porque el fragmento tiene 21 palabras. Esto es `No evaluable`.
- **Valor categórico observado:** una historia completa, con suficiente oportunidad para múltiples líneas argumentales, mantiene una sola trama principal sin subtramas. Esto puede codificarse como el valor `no_subplots` de `Subplot Integration`; en el corpus, esa opción fue más prevalente en IA (79%) que en humanos (57%). El valor sigue siendo una tendencia grupal, no una prueba de autoría.

El mismo cuidado se aplica a `no_major_withholding`, `no_direct_address`, `no_anachrony` u otras opciones explícitas del instrumento: solo se asignan cuando la definición y el texto permiten hacerlo.

## Contraevidencia

`Contraevidencia` significa **un valor observado que apunta en la dirección opuesta**, no un rasgo que simplemente no aparece. Cada contraevidencia debe tener una cita o localización textual y una interpretación alternativa.

## Regla de simetría

La oportunidad de observar un rasgo debe evaluarse con el mismo estándar para los valores humanos y los valores IA. No se puede contar como humano la falta de sensorialidad y, al mismo tiempo, ignorar la falta de referencias nombradas; ni hacer lo contrario. En muestras breves, ambas suelen quedar no evaluables.
