import * as yup from 'yup';

import { t } from '../../i18n';

export const getLoginSchema = () =>
  yup.object().shape({
    email: yup.string().email(t('validation.invalidEmail')).required(t('validation.required')),
    password: yup.string().required(t('validation.required')),
  });

export const getRegisterSchema = () =>
  yup.object().shape({
    name: yup
      .string()
      .required(t('validation.required'))
      .max(64, t('validation.maxName', { max: '64' })),
    email: yup.string().email(t('validation.invalidEmail')).required(t('validation.required')),
    password: yup
      .string()
      .required(t('validation.required'))
      .min(8, t('validation.minPassword', { min: '8' }))
      .max(32, t('validation.maxPassword', { max: '32' })),
    repeatPassword: yup.string().oneOf([yup.ref('password'), null], t(`validation.passwordMatch`)),
  });
