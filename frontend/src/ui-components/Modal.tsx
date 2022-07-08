import Box from '@mui/material/Box';
import Fade from '@mui/material/Fade';
import BaseModal, { ModalProps as BaseModalProps } from '@mui/material/Modal';

type ModalProps = Omit<BaseModalProps, 'closeAfterTransition' | 'keepMounted'> & {
  width: number | string;
};

export const Modal = ({
  'aria-labelledby': ariaLabelledBy,
  'aria-describedby': ariaDescribedBy,
  open,
  onClose,
  children,
  width,
  ...rest
}: ModalProps) => (
  <BaseModal
    aria-labelledby={ariaLabelledBy}
    aria-describedby={ariaDescribedBy}
    open={open}
    onClose={onClose}
    closeAfterTransition
    keepMounted
    {...rest}
  >
    <Fade in={open}>
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: { width },
          bgcolor: 'background.paper',
          boxShadow: 24,
          p: 4,
        }}
      >
        {children}
      </Box>
    </Fade>
  </BaseModal>
);
