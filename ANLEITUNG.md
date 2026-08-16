# Deine Website — kurze Anleitung

Deine Seite liegt unter **emilhundt.com**. Du brauchst nichts zu programmieren.
Du redest mit Claude, Claude baut es ein, du guckst es dir an, dann geht es online.

---

## Neues Gericht hochladen — in 4 Schritten

### 1. Fotos in den Ordner legen

Leg die Fotos in den Ordner **`neue-bilder`**.
Egal welches Format — iPhone-Foto, JPG, PNG, alles geht.

Gehören mehrere Fotos zum selben Gericht, nummerier sie durch:

```
steinbutt-1.jpg
steinbutt-2.jpg
```

### 2. Claude sagen, was du willst

Schreib einfach:

> **Ich möchte neue Inhalte hochladen**

Claude fragt dich dann nacheinander:

- Wie heißt das Gericht?
- Was ist drin? (die Zutaten, so wie du sie auf die Karte schreiben würdest)
- Von jemandem inspiriert? Foto von jemand anderem?

Mehr nicht. Um Abschnitt, Bildgröße und Textposition kümmert sich Claude.

### 3. Vorschau anschauen

Claude sagt dir Bescheid, wenn es eingebaut ist. Dann:

1. In **VS Code** links im Dateibaum auf **`index.html`** rechtsklicken
2. **„Open with Live Server"** anklicken
3. Der Browser geht auf — mit **⌘F** nach dem Namen des Gerichts suchen

Gefällt dir was nicht, sag es einfach:
*„Der Text ist schlecht lesbar"*, *„Pack das lieber zu den Vorspeisen"*, *„Nimm das andere Foto zuerst"*.

Die Seite lädt sich von selbst neu — du musst nur hinschauen.

### 4. Online stellen

Wenn es dir gefällt, sag **„Sieht gut aus, mach es online"**.

Claude bereitet alles vor. Einen Klick musst du selbst machen — der hängt an deinem GitHub-Login:

1. Links in VS Code auf das Symbol mit den **drei verbundenen Punkten** (Source Control)
2. Auf den blauen Knopf **Sync Changes** klicken

Nach **1–2 Minuten** ist es live auf emilhundt.com.
Wenn du es nicht siehst: **⇧⌘R** drücken (lädt die Seite komplett neu).

---

## Einmalig einrichten: Live Server

Falls beim Rechtsklick auf `index.html` **kein** „Open with Live Server" steht:

1. In VS Code links auf das Symbol mit den **vier Quadraten** (Extensions)
2. Oben **„Live Server"** eintippen
3. Beim Ergebnis von **Ritwick Dey** auf **Install** klicken

Musst du nur ein einziges Mal machen.

---

## Was du sonst noch sagen kannst

| Du willst … | Sag einfach … |
|---|---|
| Text korrigieren | „Ändere bei Steinbutt die Beschreibung zu …" |
| Gericht löschen | „Nimm das Gericht XY von der Seite" |
| Reihenfolge ändern | „Schieb Steinbutt ans Ende von Fisch" |
| Foto austauschen | „Tausch das Foto bei XY aus" — neues Foto vorher in `neue-bilder` legen |
| Catering-Event ergänzen | „Ich möchte neue Inhalte hochladen" — und dann sagen, dass es Catering ist |

---

## Die Ordner — nur zur Info

| Ordner | Was drin ist |
|---|---|
| `neue-bilder` | **Dein Ablageort.** Hier legst du neue Fotos rein. |
| `img` | Alle fertigen Fotos der Website. Nicht anfassen. |
| `Videos` | Die Videos. |
| `index.html` | Die ganze Website. Nicht von Hand ändern. |
| `css`, `js`, `tools` | Technik. Kannst du ignorieren. |

---

## Wenn was komisch aussieht

**Etwas ist kaputt und du weißt nicht warum** → sag Claude: *„Mach die letzte Änderung rückgängig."* Es gibt von allem eine Sicherung, es kann nichts verloren gehen.

**Die Seite online ist noch alt** → 2 Minuten warten, dann **⇧⌘R**.

**Du wirst nach einem GitHub-Login gefragt** → „Sign in with browser" wählen und im Browser bestätigen. Passiert nur einmal.
