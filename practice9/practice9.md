---
title: "9ª Práctica de Sistemas de Información para la Web"
author: "Ángel García Menéndez"
lang: "es-ES"
---
# Primer Ejercicio

**Miles Davis**

Como entidad escogeremos `Person`, que si bien resulta generalista, posee las suficientes propiedades para poder ajustarse a nuestras necesidades.
El conjunto de propiedades escogidas serán:

- `familyName`: Davis
- `hasOcupation`: `Occupation`: (name: jazz musician)
- `nationality`: `Country`(name: United States of America)
- `name`: Miles
- `URL`: https://www.wikidata.org/wiki/Q93341

**Barack Obama**

De la misma forma, recurriremos a `Person` para modelar al ex-presidente de EEUU. En este caso las propiedades sería:

- `familyName`: Obama
- `hasOcupation`: `Ocupation` (name: politician)
- `jobTitle`: president
- `name`: Barack
- `URL`: https://www.wikidata.org/wiki/Q76

**European Union**

El caso de la Unión Europea es particular, puesto que (discutiblemente), podría considerarse que entra dentro de la categoría de estado.
Sin embargo, tomando una aproximación conservadora, la consideraremos como `Organization`, a falta de un concepto más específico:

- `name`: European Union
- `URL`: https://www.wikidata.org/wiki/Q458

**Whashington**

Aunque no se especifica si se trata de la ciudad de Washington o del estado del mismo nombre, asumiremos que se trata de la capital de EEUU.
Un posible listado de propiedades sería:

- `name`: Washington DC
- `URL`: https://www.wikidata.org/wiki/Q61

**cambio euro/dolar**

No existe una entidad que sea _moneda_, aunque sí un tipo de cambio, que es lo que discute en el texto, y por ende se ajusta adecuadamente.
Las propiedades sería:

- `currency`: EUR
- `currentExchange`: `UnitPriceSpecification`(price: 1.3, priceCurrecy: USD)
- `URL`: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/eurofxref-graph-usd.en.html

**New York Times**

En el caso del NYT, existe la entidad `Newspaper` para describir periódicos.
Como conjunto de propiedades:

- `name`: New York Times
- `URL`: https://www.wikidata.org/wiki/Q9684

**John McCarthy**

Nuevamente, ante la falta tanto de entidades como de información en sí, se recurre a la entidad `Person`:

- `familyName`: McCarthy
- `name`: John
- `URL`: https://www.wikidata.org/wiki/Q92739

**LISP**

Schema.org ofrece una entidad denominada `ComputerLanguage`, que además se ejemplifica con el propio LISP.

- `name`: LISP
- `URL`: https://www.wikidata.org/wiki/Q132874

