import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import en from './translations/en/translation.json';

const resources = {
  en: { translation: en },
};

i18n.use(initReactI18next).init({
  resources,
  lng: 'en',
});

export const t = i18n.t.bind(i18n);
export default i18n;
