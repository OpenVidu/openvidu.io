# Shared snippets

Reusable Markdown fragments included in pages (and in other snippets) with the [`pymdownx.snippets`](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/) syntax, where the path is always relative to the **repository root**:

```markdown
--8<-- "shared/<folder>/<snippet>.md"
```

See the main [README](../README.md#adding-a-new-shared-snippet) for the full authoring rules (most importantly the **link rules**: links in snippets are root-absolute, except deployment-type-parametric ones).

## Organization

Snippets are grouped by the documentation area that consumes them. Before creating a new snippet, check whether an existing folder already covers your case, and place the new file following the same conventions:

```
shared/
├── meet/               → OpenVidu Meet docs (docs/meet/**)
│   └── webcomponent/       → WebComponent API reference (attributes, commands, events)
├── self-hosting/       → OpenVidu Platform self-hosting docs (docs/docs/self-hosting/**)
│   ├── common/             → provider-agnostic content (license intros, install-version note,
│   │                         nginx proxy guides, production-ready intro, restart/SSH instructions...)
│   ├── aws/                → AWS-specific content
│   ├── azure/              → Azure-specific content
│   ├── digitalocean/       → DigitalOcean-specific content
│   ├── gcp/                → GCP-specific content
│   ├── on-premises/        → on-premises-specific content
│   └── oracle/             → OCI-specific content
└── tutorials/          → tutorial pages of both products
    ├── application-client/ → per-platform client tutorial sections + the tabs aggregator
    ├── application-server/ → per-language server tutorial sections + the tabs aggregator
    └── openvidu-components/→ OpenVidu Components Angular tutorial sections
```

Conventions inside `self-hosting/`:

- **Provider folders mirror the provider names of the docs tree** (`docs/docs/self-hosting/{single-node,single-node-pro,elastic,ha}/<provider>/`). A snippet lives in a provider folder when all its host pages belong to that provider, no matter how many deployment types include it — that cross-deployment-type reuse is precisely why these snippets exist.
- **Filenames don't repeat the folder name**: `aws/troubleshooting.md`, not `aws/aws-troubleshooting.md`.
- **A `single-node/` subfolder inside a provider folder** holds snippets used only by that provider's `single-node/` + `single-node-pro/` pages (e.g. `aws/single-node/config.md`, `on-premises/single-node/upgrade.md`).
- **`common/` is for snippets spanning several providers** or used outside the self-hosting section (e.g. `restart-openvidu-deployment.md` is included from AI and Meet pages).
