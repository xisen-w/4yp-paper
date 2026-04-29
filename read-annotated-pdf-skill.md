# Read Annotated PDF

When the user asks to read annotations from a PDF (e.g., "read my annotations", "check my PDF comments", "看看我的批注"):

1. Run the extraction script:
   ```bash
   python /Users/wangxiang/Desktop/my_workspace/pulse/thesis/assets/read_annotations.py <pdf_path>
   ```

2. If `pymupdf` is not installed:
   ```bash
   pip install pymupdf
   ```

3. Parse the output. Each annotation has:
   - **page**: page number
   - **type**: Highlight, Text (sticky note), FreeText, StrikeOut, Underline
   - **highlighted_text**: the text that was highlighted
   - **comment**: the user's written comment

4. Group annotations by page and present them clearly.

5. For each annotation with a comment, treat it as a revision instruction:
   - If the comment says "rewrite" or "改" → rewrite that section
   - If the comment says "delete" or "删" → remove that content
   - If the comment asks a question → answer it and propose an edit
   - If it's just a highlight with no comment → flag it for the user to clarify

6. After presenting all annotations, ask: "要我按这些批注改吗？" (Should I apply these changes?)

## Example
```
User: 看看我在 main.pdf 上的批注
Agent: [runs read_annotations.py ../main.pdf]
  → Found 3 annotations:
    Page 2, Highlight: "defence specificity" — Comment: "add citation"
    Page 5, StrikeOut: "This is because..." — Comment: "rewrite, too vague"
    Page 7, Text (sticky note) — Comment: "add Pareto frontier figure here"
```
