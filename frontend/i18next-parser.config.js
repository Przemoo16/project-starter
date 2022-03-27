module.exports = {
  defaultNamespace: 'translation',
  createOldCatalogs: false,
  locales: ['en', 'pl'],
  output: 'src/translations/$LOCALE/$NAMESPACE.json',
  input: 'src/**/*.{js,jsx,ts,tsx}',
  sort: true,
};
