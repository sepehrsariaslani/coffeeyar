### Coffeeyar

Minimal coffee storefront for Peakjoy

### Installation

For a quick frontend preview in the sandbox:

```bash
cd frontend
npm install
npm run dev
```

The Vite preview includes a small local catalogue of coffee and accessory products, categories, brands, and page content, so it renders even when a Frappe backend/database is not running. To use a live Frappe API during development, start the backend and run with `VITE_DEMO_MODE=false` (optionally set `VITE_API_TARGET` to its URL).

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench install-app coffeeyar
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/coffeeyar
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
