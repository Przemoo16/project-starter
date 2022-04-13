import Box, { BoxProps } from '@mui/material/Box';

export type FormProps = Omit<BoxProps<'form'>, 'component' | 'noValidate'>;

export const Form = (props: FormProps) => <Box component="form" noValidate {...props} />;
