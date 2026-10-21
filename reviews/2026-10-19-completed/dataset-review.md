# Completed comment-by-comment annotation

All 200 labels are filled. Every comment has a saved decision, a specific reason,
and the source ID. There are zero blank labels and zero pending assistant reviews.
The completed decisions are in the repository's root `labels.csv`.

**Reviewer:** Codex (AI assistant). These completed annotations do not satisfy the
course's unaided-human or second-reviewer requirements. No training or evaluation
has run.

| Label | Completed labels | Share |
|---|---:|---:|
| analysis | 72 | 36.0% |
| unsupported | 81 | 40.5% |
| question | 47 | 23.5% |

All three classes meet the committed 15%–45% balance target for this assistant-annotated dataset. No source text or label definition was changed during this completion.

## Three difficult decisions

### Comment 26 — An adversarial question can still request information

[HN 44163144](https://news.ycombinator.com/item?id=44163144)

> Why would you do this and not just read the code yourself?

**Chosen:** question. **Alternative:** unsupported.

**Reason:** Unsupported is plausible because the wording challenges the workflow. Question is chosen because the whole comment asks for the reason for choosing it over reading code and never supplies an answer. Do not infer a settled conclusion from challenging tone alone.

### Comment 78 — Quoted evidence must support the writer's own point

[HN 48292410](https://news.ycombinator.com/item?id=48292410)

> > We build on our prior research by using three different AI detectors (Pangram, GPTZero, Copyleaks). We independently evaluate each to show that the false positive rates and average false negative rates are consistently below 2%. Each AI detector shows a similar trend.
>
> This is all bullshit, none of those actually work, and the false-positives rates are sky-high. I'm not sure how any serious person have tried out any of those services and came away with the impression of "Well, better than nothing" because literally, it seems the opposite.

**Chosen:** unsupported. **Alternative:** analysis.

**Reason:** Analysis is plausible because the comment quotes named detectors and rates below 2%. Those figures support the position the writer rejects. The rejection supplies no concrete trial, result, or source for sky-high false positives, so the main point remains unsupported. The hostile tone is not the deciding factor.

### Comment 170 — A tentative option does not necessarily settle a request

[HN 44165725](https://news.ycombinator.com/item?id=44165725)

> Since the "state of the art" seems to change every week, what's a good way to try out the current "state of the art", without spending $600? I'd love to give it a shot and be proven wrong, but I'm not going to spend 1/2 a mortgage payment on a trial.
>
> EDIT: Looks like the "Cursor" thing has a free trial. Might start there.

**Chosen:** question. **Alternative:** unsupported.

**Reason:** Unsupported is plausible because the edit could be read as answering the original request. The writer still asks for an affordable way to try the current state of the art and only says they might start with a free trial. The tentative edit leaves the main request unresolved, so question takes priority.
