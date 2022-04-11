import * as yup from 'yup';

import { t } from '../../i18n';

export const getLoginSchema = () =>
  yup.object().shape({
    email: yup.string().email(t('validation.invalidEmail')).required(t('validation.required')),
    password: yup.string().required(t('validation.required')),
  });

export const getRegisterSchema = () => {
  const passwordMinLength = +(process.env.REACT_APP_USER_PASSWORD_MIN_LENGTH || 8);
  const passwordMaxLength = +(process.env.REACT_APP_USER_PASSWORD_MAX_LENGTH || 32);
  return yup.object().shape({
    name: yup
      .string()
      .required(t('validation.required'))
      .max(64, t('validation.maxName', { max: '64' })),
    email: yup.string().email(t('validation.invalidEmail')).required(t('validation.required')),
    password: yup
      .string()
      .required(t('validation.required'))
      .min(passwordMinLength, t('validation.minPassword', { min: passwordMinLength }))
      .max(passwordMaxLength, t('validation.maxPassword', { max: passwordMaxLength })),
    repeatPassword: yup.string().oneOf([yup.ref('password'), null], t(`validation.passwordMatch`)),
  });
};

export const getResetPasswordSchema = () =>
  yup.object().shape({
    email: yup.string().email(t('validation.invalidEmail')).required(t('validation.required')),
  });

export const getSetPasswordSchema = () => {
  const passwordMinLength = +(process.env.REACT_APP_USER_PASSWORD_MIN_LENGTH || 8);
  const passwordMaxLength = +(process.env.REACT_APP_USER_PASSWORD_MAX_LENGTH || 32);
  return yup.object().shape({
    password: yup
      .string()
      .required(t('validation.required'))
      .min(passwordMinLength, t('validation.minPassword', { min: passwordMinLength }))
      .max(passwordMaxLength, t('validation.maxPassword', { max: passwordMaxLength })),
    repeatPassword: yup.string().oneOf([yup.ref('password'), null], t(`validation.passwordMatch`)),
  });
};
