# UniAds Ads Module

`src/uni_agent_template/ads.py` implements the production V2 flow.

## Request Shape

The module sends:

- `user_context`: current user message.
- `draft_response`: primary answer before sponsor injection.
- `agent_context`: agent id, name, domain, language.
- `capabilities`: supported sponsor display and trial modes.
- `layout_preferences`: compact card by default.
- `sensitivity_context`: text used for permission classification.
- `request_intent`: direct answer, recommendation, or tool use.

## Response Handling

The module returns normalized:

- `SponsorContext.raw`: full UniAds V2 response.
- `SponsorContext.card`: compact card fields.
- `SponsorContext.permission`: permission breakpoint metadata.
- `SponsorContext.matched`: whether a card is available.

## Safety Rules

- Original answer is preserved.
- Sponsor card is appended after the answer.
- Permission-required actions are surfaced as prompts.
- Network/API errors return an empty sponsor context.
- Requests ignore broken desktop proxy env variables by using `session.trust_env = False`.
