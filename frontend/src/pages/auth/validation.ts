import * as yup from 'yup';

import { t } from '../../i18n';

export const getLoginSchema = () =>
  yup.object().shape({
    email: yup.string().email(t('validation.invalidEmail')).required(t('validation.required')),
    password: yup.string().required(t('validation.required')),
  });
